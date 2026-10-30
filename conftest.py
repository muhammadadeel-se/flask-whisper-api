import os
import pytest

# Ensure dummy API key is always set before app.py or tests are imported
os.environ["OPENAI_API_KEY"] = "mock-key-for-testing"

@pytest.fixture(autouse=True)
def mock_env_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "mock-key-for-testing")