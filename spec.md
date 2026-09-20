# AI Evaluation Pipeline Specification

## 1. Executive Summary
This project implements a production-grade AI evaluation pipeline designed for the Waqas AI team. It provides a structured, deterministic-first framework to assess LLM assistant responses, ensuring high-quality, policy-adherent customer support through modular, scalable engineering.

## 2. Design Approach & Architecture
*   **Modular Pipeline**: Implements a sequential state machine (`INIT` -> `RESULTS_FINALIZED`) to process cases, run deterministic rules, perform LLM evaluation, and aggregate final scores.
*   **UI/UX**: Features a **Streamlit-based dashboard** for intuitive visualization of pipeline stages, artifacts, and interactive pipeline orchestration.
*   **Observability**: Detailed audit trails are maintained via `llm_calls.jsonl`, logging every interaction with metadata, timestamps, and model provenance.
*   **Auditor-Friendly**: All intermediate artifacts (`rule_checks.json`, `llm_evaluations.json`, `final_scores.json`) are persisted, allowing for idempotent reruns and complete transparency for human auditors.

## 3. Resilience & Latency
*   **Latency Handling**: All I/O-bound LLM operations are executed using asynchronous-ready patterns.
*   **Circuit Breakers & Retries**: Utilizes `tenacity` with exponential backoff for API calls. If an LLM call fails repeatedly, the pipeline logs the failure state and proceeds, ensuring partial system availability and graceful degradation.
*   **Fallback Mechanism**: A built-in `MockEvaluator` activates automatically when no valid API key is present, ensuring the pipeline remains runnable in offline/local dev environments.

## 4. Security & Guardrails
*   **Injection Prevention**: System prompts are architected with explicit delimiters (e.g., `"""USER_MESSAGE: ... """`) to encapsulate user input, neutralizing prompt injection vectors.
*   **Deterministic Integrity**: Critical policy checks are computed via code-based heuristics before calling the LLM, reducing dependency on model judgment for safety-critical constraints.

## 5. Implementation Stack
*   **Runtime**: Python (FastAPI backend for orchestration, Streamlit for UI).
*   **Validation**: Pydantic for rigid JSON schema enforcement at every stage.
*   **Model Provider**: Google Gemini (Standardized via `google-genai`).

## 6. Validation & Testing
*   **Integrity Checks**: `python validate.py` asserts artifact existence, JSON validity, and lineage, ensuring the final report is grounded in the source data.
