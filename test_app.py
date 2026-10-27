import os
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_transcribe_wav_file(client):
    audio_path = os.path.join('tests', 'fixtures', 'sample.wav')
    assert os.path.exists(audio_path), "Sample audio file missing from tests/fixtures/"
    
    with open(audio_path, 'rb') as audio_file:
        response = client.post('/transcribe', data={'file': audio_file})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'transcript' in data
    assert isinstance(data['transcript'], str)