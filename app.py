import os
import tempfile
from flask import Flask, request, jsonify
import whisper

app = Flask(__name__)

# Pre-load Whisper model at startup to prevent UI freezing and timeouts
MODEL = whisper.load_model("tiny")

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    # 1. Check if file key exists in request
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    # 2. Check if file is empty
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # 3. Check if file extension is .wav
    if not file.filename.lower().endswith('.wav'):
        return jsonify({"error": "Invalid file format. Only .wav files are allowed."}), 400

    # Temporary file storage for safe I/O
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        file.save(temp_file.name)
        temp_path = temp_file.name

    try:
        result = MODEL.transcribe(temp_path)
        transcript_text = result.get("text", "").strip()
        
        return jsonify({"transcript": transcript_text}), 200

    except Exception as e:
        return jsonify({"error": f"Transcription failed: {str(e)}"}), 500

    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)