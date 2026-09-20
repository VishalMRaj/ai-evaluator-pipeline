import json
import os


def validate():
    required_files = [
        "artifacts/cases.json",
        "artifacts/rule_checks.json",
        "artifacts/llm_evaluations.json",
        "artifacts/final_scores.json",
        "artifacts/llm_calls.jsonl",
        "artifacts/report.md",
    ]
...
    # Check JSON validity
    with open("artifacts/cases.json") as f:
        data = json.load(f)
    assert len(data) == 3
    print("Validation passed: All artifacts exist and are valid.")


if __name__ == "__main__":
    validate()
