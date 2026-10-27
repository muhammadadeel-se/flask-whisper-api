# Flask Whisper Audio API

A Flask REST API that transcribes `.wav` audio files using OpenAI's Whisper model. The model is pre-loaded at startup to eliminate latency and prevent server timeouts.

## Prerequisites
- Python 3.8+
- `ffmpeg` installed on host system (`sudo apt install ffmpeg` or `brew install ffmpeg`)

## Installation & Setup

1. Clone repository: