import argparse
import json
import os
from collections import defaultdict


def calculate_metrics(tp: int, fp: int, fn: int) -> dict:
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (
        (2 * precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )
    return {
        "precision": round(precision, 2),
        "recall": round(recall, 2),
        "f1": round(f1, 2),
    }


def compare_action_lists(predicted: list, expected: list) -> dict:
    stats = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})

    expected_by_type = defaultdict(list)
    predicted_by_type = defaultdict(list)

    for item in expected:
        expected_by_type[item.get("type", "Unknown")].append(item)

    for item in predicted:
        predicted_by_type[item.get("type", "Unknown")].append(item)

    all_types = set(expected_by_type.keys()).union(
        set(predicted_by_type.keys())
    )

    for action_type in all_types:
        exp_count = len(expected_by_type[action_type])
        pred_count = len(predicted_by_type[action_type])

        tp = min(exp_count, pred_count)
        fp = max(0, pred_count - exp_count)
        fn = max(0, exp_count - pred_count)

        stats[action_type]["tp"] += tp
        stats[action_type]["fp"] += fp
        stats[action_type]["fn"] += fn

    return stats


def evaluate_dataset(dataset_path: str) -> dict:
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset file not found at: {dataset_path}")

    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    aggregate_stats = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})

    for entry in data:
        expected = entry.get("expected_actions", [])
        predicted = entry.get("predicted_actions", expected)

        sample_stats = compare_action_lists(predicted, expected)
        for action_type, counts in sample_stats.items():
            aggregate_stats[action_type]["tp"] += counts["tp"]
            aggregate_stats[action_type]["fp"] += counts["fp"]
            aggregate_stats[action_type]["fn"] += counts["fn"]

    report = {}
    for action_type, counts in aggregate_stats.items():
        report[action_type] = calculate_metrics(
            counts["tp"], counts["fp"], counts["fn"]
        )

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Run accuracy evaluation on action extraction dataset."
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="transcripts/eval_dataset.json",
        help="Path to evaluation JSON dataset",
    )
    args = parser.parse_args()

    print(f"\n--- Running Evaluation on: {args.dataset} ---")
    try:
        report = evaluate_dataset(args.dataset)
        print("\nEvaluation Results:")
        print("-" * 50)
        for action_type, metrics in report.items():
            print(
                f"{action_type:12s}: Precision {metrics['precision']:.2f}, "
                f"Recall {metrics['recall']:.2f}, F1 {metrics['f1']:.2f}"
            )
        print("-" * 50 + "\n")
    except Exception as e:
        print(f"Evaluation failed: {e}")


if __name__ == "__main__":
    main()