import os
import json
import tempfile
from flask import Flask, request, jsonify
import whisper

app = Flask(__name__)

# Pre-load Whisper model at startup
MODEL = whisper.load_model("tiny")

# Directory for storing output transcripts
TRANSCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'transcripts')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.lower().endswith('.wav'):
        return jsonify({"error": "Invalid file format. Only .wav files are allowed."}), 400

    # Temporary file storage for safe audio I/O
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        file.save(temp_file.name)
        temp_path = temp_file.name

    try:
        result = MODEL.transcribe(temp_path)
        transcript_text = result.get("text", "").strip()

        # Ensure transcripts directory exists
        os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

        # Save transcript to JSON file named after uploaded WAV file
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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)