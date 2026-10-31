import json
import pytest
from app import app


@pytest.fixture
def test_client(tmp_path):
    # Setup temporary actions.json inside pytest's isolated tmp_path directory
    actions_file = tmp_path / "actions.json"

    initial_data = [
        {
            "id": "act_101",
            "description": "Initial Task One",
            "status": "pending",
        },
        {
            "id": "act_102",
            "description": "Initial Task Two",
            "status": "pending",
        },
    ]
    actions_file.write_text(json.dumps(initial_data), encoding="utf-8")

    app.config["TESTING"] = True
    app.config["ACTIONS_FILE"] = str(actions_file)

    with app.test_client() as client:
        yield client


def test_root_redirects_to_confirm(test_client):
    response = test_client.get("/")
    assert response.status_code == 302
    assert "/confirm" in response.headers["Location"]


def test_ui_displays_actions_with_edit_fields(test_client):
    response = test_client.get("/confirm")
    assert response.status_code == 200

    html_content = response.data.decode("utf-8")
    assert "Initial Task One" in html_content
    assert "Initial Task Two" in html_content
    assert '<input type="text"' in html_content
    assert '<select id="status-act_101"' in html_content


def test_editing_action_updates_json_file(test_client, tmp_path):
    actions_file = tmp_path / "actions.json"

    payload = {
        "actions": [
            {
                "id": "act_101",
                "description": "Updated Task One Description",
                "status": "confirmed",
            },
            {
                "id": "act_102",
                "description": "Initial Task Two",
                "status": "pending",
            },
        ]
    }

    response = test_client.post("/confirm", json=payload)
    assert response.status_code == 200
    assert response.json["status"] == "success"

    stored_file_data = json.loads(actions_file.read_text(encoding="utf-8"))
    assert len(stored_file_data) == 2
    assert stored_file_data[0]["id"] == "act_101"
    assert (
        stored_file_data[0]["description"] == "Updated Task One Description"
    )
    assert stored_file_data[0]["status"] == "confirmed"