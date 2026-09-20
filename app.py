import streamlit as st
import json
import pandas as pd
import os

st.set_page_config(page_title="AI Evaluator Pipeline", layout="wide")

st.title("🤖 AI Evaluator Pipeline Dashboard")


# Load data helper
@st.cache_data
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return None


# Sidebar for navigation
st.sidebar.header("Pipeline Stages")
stage = st.sidebar.radio(
    "Select View",
    ["Overview", "Cases & Rule Checks", "LLM Evaluations", "Final Scores"],
)

# Load all artifacts
cases = load_data("artifacts/cases.json")
rules = load_data("artifacts/rule_checks.json")
evals = load_data("artifacts/llm_evaluations.json")
scores = load_data("artifacts/final_scores.json")

if stage == "Overview":
    st.header("Pipeline Status")
    if scores:
        df = pd.DataFrame(scores)
        st.metric("Total Cases Processed", len(df))
        st.table(df)
    else:
        st.warning("Pipeline has not been run or data is missing.")

elif stage == "Cases & Rule Checks":
    st.header("Deterministic Rule Checks")
    if rules:
        df_rules = pd.DataFrame(rules)
        st.dataframe(df_rules)
    else:
        st.info("No rule checks found.")

elif stage == "LLM Evaluations":
    st.header("LLM Judgment")
    if evals:
        df_evals = pd.DataFrame(evals)
        st.dataframe(df_evals)
    else:
        st.info("No LLM evaluations found.")

elif stage == "Final Scores":
    st.header("Final Aggregated Scores")
    if scores:
        df_scores = pd.DataFrame(scores)
        st.bar_chart(df_scores.set_index("case_id")["score"])
        st.table(df_scores)
    else:
        st.info("No final scores found.")

st.sidebar.markdown("---")
if st.sidebar.button("Run Pipeline"):
    # This would trigger the backend scripts
    st.sidebar.info("Running pipeline...")
    # Force reload data
    st.cache_data.clear()

    os.system(
        "python src/rules.py && python src/evaluator.py && python src/scorer.py && python src/reporter.py"
    )
    st.sidebar.success("Pipeline Run Complete!")
    st.rerun()
