import json
from src.models import RuleCheck, LLMEvaluation, FinalScore
from typing import List


def aggregate_scores(
    rule_results: List[RuleCheck], llm_results: List[LLMEvaluation]
) -> List[FinalScore]:
    final_scores = []

    # Map them for easy lookup
    rules_map = {r.case_id: r for r in rule_results}
    llm_map = {e.case_id: e for e in llm_results}

    for case_id in rules_map:
        rule = rules_map[case_id]
        llm = llm_map[case_id]

        score = 100
        explanation = []

        # Scoring Logic
        if llm.policy_adherence == "fail":
            score = 0
            explanation.append("Automatic failure: Policy breach identified by LLM.")
        elif rule.absolute_guarantee_detected:
            score -= 40
            explanation.append("Deducted 40: Risky absolute language detected.")

        if not rule.required_points_covered:
            score -= 30
            explanation.append("Deducted 30: Missing required points.")

        if llm.risk_level == "high":
            score = min(score, 20)
            explanation.append("Capped at 20: High risk level.")

        score = max(score, 0)

        status = "pass" if score >= 80 else ("review" if score >= 50 else "fail")

        final_scores.append(
            FinalScore(
                case_id=case_id,
                score=score,
                status=status,
                explanation=" | ".join(explanation)
                if explanation
                else "No issues identified.",
            )
        )

    return final_scores


if __name__ == "__main__":
    with open("artifacts/rule_checks.json", "r") as f:
        rules = [RuleCheck(**r) for r in json.load(f)]
    with open("artifacts/llm_evaluations.json", "r") as f:
        llms = [LLMEvaluation(**e) for e in json.load(f)]

    scores = aggregate_scores(rules, llms)
    with open("artifacts/final_scores.json", "w") as f:
        json.dump([s.model_dump() for s in scores], f, indent=2)
