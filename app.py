import os
import tempfile
from flask import Flask, request, jsonify
import whisper

app = Flask(__name__)

# Pre-load Whisper model at startup
MODEL = whisper.load_model("tiny")

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if not file.filename.lower().endswith('.wav'):
        return jsonify({"error": "Only .wav files allowed"}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        file.save(temp_file.name)
        temp_path = temp_file.name

    try:
        result = MODEL.transcribe(temp_path)
        return jsonify({"transcript": result.get("text", "").strip()})
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)