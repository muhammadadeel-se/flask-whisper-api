import json
import os
from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["ACTIONS_FILE"] = os.getenv("ACTIONS_FILE", "actions.json")

DEFAULT_ACTIONS = [
    {
        "id": "act_001",
        "description": "Verify environment variables",
        "status": "pending",
    },
    {
        "id": "act_002",
        "description": "Run automated test suite",
        "status": "pending",
    },
]


def load_actions():
    filepath = app.config["ACTIONS_FILE"]
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_ACTIONS, f, indent=2)
        return DEFAULT_ACTIONS

    with open(filepath, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


@app.route("/")
def index():
    # 1. Root route redirects to /confirm
    return redirect(url_for("confirm"))


@app.route("/confirm", methods=["GET", "POST"])
def confirm():
    if request.method == "POST":
        data = request.get_json()

        if not data or "actions" not in data:
            return (
                jsonify(
                    {"error": "Invalid payload format. Expected key 'actions'."}
                ),
                400,
            )

        actions = data["actions"]
        if not isinstance(actions, list):
            return jsonify({"error": "Field 'actions' must be a list."}), 400

        filepath = app.config["ACTIONS_FILE"]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(actions, f, indent=2)

        return jsonify({"status": "success", "count": len(actions)}), 200

    actions = load_actions()
    return render_template("index.html", actions=actions)


if __name__ == "__main__":
    app.run(debug=True)