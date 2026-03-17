import json
from statistics import mean, median
from pathlib import Path

def build_report(retrieval_results, generation_results, output_dir="reports"):
    Path(output_dir).mkdir(exist_ok=True)

    recall_scores = [r["recall"] for r in retrieval_results]
    grounding_scores = [g["grounding"] for g in generation_results]
    latencies = [g["latency"] for g in generation_results]

    report = {
        "retrieval": {
            "mean_recall": mean(recall_scores),
            "median_recall": median(recall_scores),
            "min_recall": min(recall_scores),
            "max_recall": max(recall_scores)
        },
        "generation": {
            "mean_grounding": mean(grounding_scores),
            "median_grounding": median(grounding_scores)
        },
        "latency": {
            "mean": mean(latencies),
            "median": median(latencies)
        }
    }

    path = Path(output_dir) / "evaluation_report.json"

    with open(path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Report written to {path}")