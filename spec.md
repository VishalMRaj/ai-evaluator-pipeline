# AI Evaluation Pipeline: Technical Specification & Contract

## 1. Vision & Executive Summary
The AI Evaluation Pipeline is an enterprise-grade automated framework built for the Waqas AI team. It establishes a **deterministic-first, LLM-augmented** evaluation protocol, ensuring that customer support interactions are scored with precision, reproducibility, and security.

## 2. Technical Contracts & Schema
The pipeline enforces strict data contracts using Pydantic models. Every artifact is validated against these schemas to ensure end-to-end data integrity.

### Input Data Contract (`cases.json`)
- **Case**: Contains `case_id`, `user_message`, `assistant_response`, and `policy_context` (a nested structure defining `allowed_actions`, `disallowed_actions`, and `required_points`).

### Output Data Contract (`llm_evaluations.json`)
- **EvaluationSchema**:
    - `case_id`: String
    - `policy_adherence`: Enum ("pass", "warning", "fail")
    - `customer_helpfulness`: Enum ("pass", "warning", "fail")
    - `risk_level`: Enum ("low", "medium", "high")
    - `reasoning`: List[String]
    - `policy_violations`: List[String]
    - `recommended_fix`: String

## 3. Core Engine Mechanics
*   **Deterministic Rule Processor (`rules.py`)**: Executes before any LLM call. Maps assistant responses against PII regex patterns, keyword-based risk heuristics (e.g., "guarantee", "instantly"), and mandatory policy point coverage.
*   **LLM Judgment Layer (`evaluator.py`)**: Uses **Gemini 3.1 Flash-Lite** via structured JSON enforcement. Prompt engineering is governed by strict delimiter-based guardrails (`"""USER_MESSAGE"""`) to negate prompt injection attempts.
*   **Scoring Aggregator (`scorer.py`)**: A purely code-driven aggregation engine.
    *   *Formula*: `Score = 100 - (Policy_Breach_Weight) - (Missing_Points_Weight)`.
    *   *Constraint*: High-risk classifications automatically cap the maximum possible score to 20, forcing a "Fail" or "Review" status.

## 4. Resilience & Fallback Contracts
*   **API-less Fallback Mode**: The system provides a `MockEvaluator` interface that returns synthetically generated assessment objects if the environment lacks a valid `GEMINI_API_KEY`.
*   **Bounded Retry Logic**: Employs exponential backoff (via `tenacity`) for all remote network calls, ensuring the pipeline can handle intermittent 503/server-overload errors.

## 5. Observability & Auditing
*   **Operational Logs**: `llm_calls.jsonl` tracks the full provenance of every LLM call, including timestamps, model versioning, prompt hashes, and input-output artifact associations.
*   **Reproducibility**: The system architecture supports idempotent reruns, where intermediate artifacts are treated as append-only logs for auditors to trace the decision history of any specific case.

## 6. Validation Integrity
The pipeline ships with a rigorous `validate.py` suite. Before finalization, it validates:
1.  **Existence**: All required JSON files are materialized.
2.  **Schema Validity**: All artifacts conform to the established Pydantic contracts.
3.  **Lineage**: The number of evaluations matches the input case count, and the final scores correctly reference existing rule-check and evaluation results.

## 7. UI Layer & Orchestration
The UI acts as the command-and-control center for the AI Engineering team:
*   **Technology**: Built with **Streamlit** for reactive data visualization.
*   **Orchestration**: The UI exposes a **FastAPI backend** (running on `uvicorn`) that serves as the controller for the pipeline.
*   **Pipeline Lifecycle**:
    1.  **Trigger**: Clicking "Run Pipeline" invokes the orchestrator via REST API.
    2.  **Execution**: The orchestrator triggers the sequence of scripts (`rules.py` -> `evaluator.py` -> `scorer.py` -> `reporter.py`) as independent processes.
    3.  **Visualization**: Upon completion, the Streamlit dashboard automatically reloads and renders the generated `artifacts/` contents.
*   **Execution Command**: 
    - **Backend**: `uvicorn src.main:app --port 8000`
    - **UI**: `streamlit run app.py --server.port 8501`
