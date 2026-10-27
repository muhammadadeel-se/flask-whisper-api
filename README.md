# Flask Whisper & Action Extraction API

A Flask REST API that transcribes `.wav` audio files using OpenAI's Whisper model and extracts structured action items using OpenAI's Structured Outputs (Pydantic schemas).

## System Prerequisites

OpenAI Whisper requires **FFmpeg** to process audio files:
- **Windows:** `winget install Gyan.FFmpeg`
- **macOS:** `brew install ffmpeg`
- **Linux (Ubuntu/Debian):** `sudo apt update && sudo apt install -y ffmpeg`

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/muhammadadeel-se/flask-whisper-api.git](https://github.com/muhammadadeel-se/flask-whisper-api.git)
   cd flask-whisper-api