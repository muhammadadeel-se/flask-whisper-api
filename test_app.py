import os
import json
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_transcribe_wav_file(client):
    audio_path = os.path.join('tests', 'fixtures', 'sample.wav')
    assert os.path.exists(audio_path), "Sample audio file missing"

    with open(audio_path, 'rb') as audio_file:
        response = client.post('/transcribe', data={'file': (audio_file, 'sample.wav')})

    assert response.status_code == 200
    data = response.get_json()
    assert 'transcript' in data

    # Verify JSON file creation in transcripts/ directory
    json_path = os.path.join('transcripts', 'sample.json')
    assert os.path.exists(json_path), "Transcript JSON file was not saved to transcripts/"

    with open(json_path, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
        assert saved_data['filename'] == 'sample.wav'
        assert 'transcript' in saved_data