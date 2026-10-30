# Flask Whisper & Action Extraction API

A Flask REST API that transcribes `.wav` audio files using OpenAI's Whisper model and extracts structured action items using OpenAI GPT models.

---

## 🔑 OpenAI API Key Configuration & Usage

The `/extract` endpoint requires an active **OpenAI API Key** to communicate with OpenAI's `gpt-4o-mini` model for structured action extraction.

### Option 1: Using a `.env` File (Recommended)
Create a `.env` file in the root directory of your project:

```env
OPENAI_API_KEY=your_openai_api_key_here