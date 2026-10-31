import json
import pytest
from evaluate import calculate_metrics, compare_action_lists, evaluate_dataset


def test_calculate_metrics_perfect_score():
    metrics = calculate_metrics(tp=5, fp=0, fn=0)
    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 1.0
    assert metrics["f1"] == 1.0


def test_calculate_metrics_zero_division():
    metrics = calculate_metrics(tp=0, fp=0, fn=0)
    assert metrics["precision"] == 0.0
    assert metrics["recall"] == 0.0
    assert metrics["f1"] == 0.0


def test_compare_action_lists_partial_match():
    expected = [
        {"type": "Schedule", "description": "Meeting A"},
        {"type": "Task", "description": "Task B"},
    ]
    predicted = [
        {"type": "Schedule", "description": "Meeting A"},
        {"type": "Schedule", "description": "Extra Meeting"},
    ]

    stats = compare_action_lists(predicted, expected)

    assert stats["Schedule"]["tp"] == 1
    assert stats["Schedule"]["fp"] == 1
    assert stats["Task"]["tp"] == 0
    assert stats["Task"]["fn"] == 1


def test_evaluate_dataset_file(tmp_path):
    dataset_file = tmp_path / "test_eval.json"
    sample_data = [
        {
            "id": "1",
            "transcript": "Test transcript",
            "expected_actions": [{"type": "Schedule"}],
            "predicted_actions": [{"type": "Schedule"}],
        }
    ]
    dataset_file.write_text(json.dumps(sample_data), encoding="utf-8")

    report = evaluate_dataset(str(dataset_file))
    assert "Schedule" in report
    assert report["Schedule"]["f1"] == 1.0