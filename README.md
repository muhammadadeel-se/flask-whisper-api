# Confirmation UI and Persistence

A Flask-based web application that displays a list of action items with editable fields, allowing users to modify descriptions and statuses, and persist the confirmed updates directly to `actions.json`.

---

## Features & Acceptance Criteria

- **Editable UI**: Renders a list of action items with input fields for description and dropdowns for status.
- **JSON Persistence**: Submitting edits sends a POST request via JavaScript `fetch()` to `/confirm`, updating `actions.json`.
- **Automated Test Suite**: Includes `pytest` tests using Pytest's `tmp_path` fixture to verify UI rendering and file persistence in total isolation from production data.

---

## Project Structure

```text
.
├── app.py              # Flask server and file persistence routing
├── templates/
│   └── index.html      # Jinja HTML UI with embedded edit form and JavaScript submit logic
├── test_app.py         # Pytest suite verifying UI rendering and file updates
├── actions.json        # Stored action records (auto-generated if missing)
└── README.md           # Project documentation
## Accuracy Evaluation

Run the accuracy evaluation CLI script to benchmark model predictions against the ground truth dataset:

```bash
python evaluate.py --dataset transcripts/eval_dataset.json