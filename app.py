import json
import os
from flask import Flask, jsonify, render_template, request
from openai import OpenAI

app = Flask(__name__)

# Initialize OpenAI Client (uses OPENAI_API_KEY environment variable)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

CONFIRMED_ACTIONS_FILE = os.path.join("data", "confirmed_actions.json")
os.makedirs("data", exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_audio():
    """Endpoint to upload an audio file and generate its transcript using Whisper API."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    audio_file = request.files["file"]
    if audio_file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    upload_folder = os.path.join("transcripts", "uploads")
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, audio_file.filename)
    audio_file.save(file_path)

    try:
        with open(file_path, "rb") as f:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", file=f
            )
        transcript_text = transcription.text
        return jsonify(
            {
                "status": "success",
                "filename": audio_file.filename,
                "transcript": transcript_text,
            }
        )
    except Exception as e:
        return jsonify({"error": f"Audio transcription failed: {str(e)}"}), 500


@app.route("/extract", methods=["POST"])
def extract_actions():
    """Endpoint to extract structured action items from transcript text."""
    data = request.get_json() or {}
    transcript = data.get("transcript", "")

    if not transcript:
        return jsonify({"error": "Transcript text is required"}), 400

    prompt = f"""
Analyze the following transcript and extract action items. 
Categorize each action into one of these types: Schedule, Task, Reminder, Follow-up.

Return ONLY a valid JSON array of objects with keys "type" and "description".

Transcript:
"{transcript}"
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        content = response.choices[0].message.content.strip()

        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        content = content.strip()

        actions = json.loads(content)
        return jsonify({"transcript": transcript, "actions": actions})
    except Exception as e:
        return jsonify({"error": f"Action extraction failed: {str(e)}"}), 500


@app.route("/confirm", methods=["POST"])
def confirm_actions():
    """Endpoint to confirm and store extracted action items."""
    data = request.get_json() or {}
    confirmed_actions = data.get("actions", [])

    if not isinstance(confirmed_actions, list):
        return jsonify({"error": "Actions must be a list"}), 400

    existing = []
    if os.path.exists(CONFIRMED_ACTIONS_FILE):
        try:
            with open(CONFIRMED_ACTIONS_FILE, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except Exception:
            existing = []

    existing.extend(confirmed_actions)

    with open(CONFIRMED_ACTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2)

    return jsonify(
        {
            "status": "success",
            "message": "Actions confirmed and stored successfully",
            "total_saved": len(existing),
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)