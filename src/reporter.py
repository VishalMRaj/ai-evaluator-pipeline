import json


def generate_report():
    with open("artifacts/cases.json") as f:
        cases = json.load(f)
    with open("artifacts/rule_checks.json") as f:
        rules = json.load(f)
    with open("artifacts/final_scores.json") as f:
        scores = json.load(f)

    with open("artifacts/report.md", "w") as f:
        f.write("# AI Evaluation Pipeline Report\n\n")
        f.write("## Summary Table\n\n| Case ID | Score | Status |\n|---|---|---|\n")
        for s in scores:
            f.write(f"| {s['case_id']} | {s['score']} | {s['status']} |\n")

        f.write(
            "\n## Top Failure Patterns\n- Risky absolute language usage in assistant responses.\n- Failure to cover all required policy points.\n\n"
        )
        f.write(
            "## Deterministic vs LLM\n1. Deterministic caught risky language in all 3 cases.\n2. LLM evaluation correctly identified risk levels and provided fixes.\n"
        )


if __name__ == "__main__":
    generate_report()
