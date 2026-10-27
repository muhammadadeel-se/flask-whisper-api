# Flask Whisper Audio API

A Flask REST API that transcribes `.wav` audio files using OpenAI's Whisper model. The model is pre-loaded at startup to eliminate latency and prevent server timeouts.

## Prerequisites
- Python 3.8+
- `ffmpeg` installed on host system (`sudo apt install ffmpeg` or `brew install ffmpeg`)

## Installation & Setup

1. Clone repository:
### System Dependencies
OpenAI Whisper requires **FFmpeg** to process audio files:
- **Windows:** `winget install Gyan.FFmpeg`
- **macOS:** `brew install ffmpeg`
- **Linux (Ubuntu/Debian):** `sudo apt update && sudo apt install -y ffmpeg`
## Execution & Running the App

To start the Flask development server on `http://127.0.0.1:5000`:

```bash
python app.py