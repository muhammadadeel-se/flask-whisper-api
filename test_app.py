import os
import json
import pytest
from unittest.mock import patch, MagicMock

# Set dummy key for test environment
os.environ["OPENAI_API_KEY"] = "mock-key-for-testing"

from app import app
from schemas import ActionItem, ActionItemList

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

    json_path = os.path.join('transcripts', 'sample.json')
    assert os.path.exists(json_path), "Transcript JSON file was not saved to transcripts/"


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

    with patch('app.client.beta.chat.completions.parse') as mock_parse:
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(parsed=ActionItemList.model_validate(mock_payload)))
        ]
        mock_parse.return_value = mock_response

        response = client.post(
            '/extract-actions',
            json={"transcript": "Adeel needs to prepare project slides by Friday with high priority."}
        )

        assert response.status_code == 200
        json_data = response.get_json()

        validated_obj = ActionItemList.model_validate(json_data)
        assert len(validated_obj.actions) == 1
        assert validated_obj.actions[0].task == "Prepare project slides"
        assert validated_obj.actions[0].assignee == "Adeel"