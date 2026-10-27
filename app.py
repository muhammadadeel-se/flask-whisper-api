import os
import json
import tempfile
from flask import Flask, request, jsonify
import whisper
from openai import OpenAI
from schemas import ActionItem, ActionItemList

app = Flask(__name__)

# Pre-load Whisper model at startup
MODEL = whisper.load_model("tiny")
TRANSCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'transcripts')

# Initialize OpenAI Client (with fallback key for testing)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "mock-key-for-testing"))

SYSTEM_PROMPT = """You are an executive assistant specializing in meeting analysis.
Your job is to parse the input transcript and extract all explicit or implied action items.
Output strictly according to the requested JSON schema. If no action items exist, return an empty actions list."""


@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.lower().endswith('.wav'):
        return jsonify({"error": "Invalid file format. Only .wav files are allowed."}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        file.save(temp_file.name)
        temp_path = temp_file.name

    try:
        result = MODEL.transcribe(temp_path)
        transcript_text = result.get("text", "").strip()

        os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

        base_name = os.path.splitext(os.path.basename(file.filename))[0]
        json_filename = f"{base_name}.json"
        json_path = os.path.join(TRANSCRIPTS_DIR, json_filename)

        transcript_data = {
            "filename": file.filename,
            "transcript": transcript_text
        }

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(transcript_data, f, indent=4)

        return jsonify({"transcript": transcript_text}), 200

    except Exception as e:
        return jsonify({"error": f"Transcription failed: {str(e)}"}), 500

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.route('/extract-actions', methods=['POST'])
def extract_actions():
    data = request.get_json()
    if not data or 'transcript' not in data:
        return jsonify({"error": "Missing 'transcript' in request body"}), 400

    transcript_text = data['transcript'].strip()
    if not transcript_text:
        return jsonify({"error": "Transcript text cannot be empty"}), 400

    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": transcript_text}
            ],
            response_format=ActionItemList
        )

        parsed_response: ActionItemList = completion.choices[0].message.parsed
        validated_data = ActionItemList.model_validate(parsed_response)

        return jsonify(validated_data.model_dump()), 200

    except Exception as e:
        return jsonify({"error": f"Action extraction failed: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)