import os
import json
import pytest
from unittest.mock import patch, MagicMock

os.environ["OPENAI_API_KEY"] = "sk-mock-key-for-unit-testing"

import app as flask_app
from app import app
from schemas import ActionItem, ActionItemList

flask_app.client = MagicMock()


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_transcribe_wav_file(client):
    audio_path = os.path.join('tests', 'fixtures', 'sample.wav')
    assert os.path.exists(audio_path), "Sample audio file missing"

    with patch('app.MODEL.transcribe') as mock_transcribe:
        mock_transcribe.return_value = {"text": "This is a valid test transcript."}

        with open(audio_path, 'rb') as audio_file:
            response = client.post('/transcribe', data={'file': (audio_file, 'sample.wav')})

        assert response.status_code == 200
        data = response.get_json()
        assert 'transcript' in data
        assert len(data['transcript'].strip()) > 0

    json_path = os.path.join('transcripts', 'sample.json')
    assert os.path.exists(json_path), "Transcript JSON file was not saved to transcripts/"


def test_transcribe_empty_audio_returns_error(client):
    audio_path = os.path.join('tests', 'fixtures', 'sample.wav')

    with patch('app.MODEL.transcribe') as mock_transcribe:
        mock_transcribe.return_value = {"text": "   "}

        with open(audio_path, 'rb') as audio_file:
            response = client.post('/transcribe', data={'file': (audio_file, 'sample.wav')})

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data


def test_action_extraction_endpoint(client):
    mock_payload = {
        "actions": [
            {
                "task": "Prepare project slides",
                "assignee": "Adeel",
                "due_date": "Friday",
                "priority": "high"
            }
        ]
    }

    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(parsed=ActionItemList.model_validate(mock_payload)))
    ]
    flask_app.client.beta.chat.completions.parse.return_value = mock_response

    response = client.post(
        '/extract-actions',
        json={"transcript": "Adeel needs to prepare project slides by Friday with high priority."}
    )

    assert response.status_code == 200
    json_data = response.get_json()

    validated_obj = ActionItemList.model_validate(json_data)
    assert len(validated_obj.actions) == 1
    assert validated_obj.actions[0].task == "Prepare project slides"