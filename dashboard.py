import streamlit as st
import pandas as pd

# Load analytics data
df = pd.read_csv("data/processed/analytics_dataset.csv")

# -----------------------------
# PAGE
# -----------------------------

st.set_page_config(
    page_title="NIMCET Performance Analytics",
    layout="wide"
)

st.title("NIMCET Performance Analytics Dashboard")
st.write("Analysis of candidate preparation and NIMCET performance")

# -----------------------------
# KPI SECTION
# -----------------------------

st.header("Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Candidates", len(df))
col2.metric("Average Marks", round(df["nimcet_total_marks"].mean(), 2))
col3.metric("Best Rank", int(df["nimcet_rank"].min()))
col4.metric("Avg Study Hours", round(df["study_hours_daily"].mean(), 2))

# -----------------------------
# PERFORMANCE ANALYSIS
# -----------------------------

st.header("Performance Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Study Hours vs Average Marks")

    study = (
        df.groupby("study_hours_daily")["nimcet_total_marks"]
        .mean()
        .reset_index()
    )

    st.line_chart(
        study.set_index("study_hours_daily")
    )

with col2:
    st.subheader("Preparation Months vs Average Marks")

    preparation = (
        df.groupby("preparation_months")["nimcet_total_marks"]
        .mean()
        .reset_index()
    )

    st.line_chart(
        preparation.set_index("preparation_months")
    )

# -----------------------------
# MOCK TEST ANALYSIS
# -----------------------------

st.subheader("Mock Test Performance")

mock = (
    df.groupby("mock_tests_count")["nimcet_total_marks"]
    .mean()
    .reset_index()
)

st.line_chart(
    mock.set_index("mock_tests_count")
)

# -----------------------------
# SUBJECT PERFORMANCE
# -----------------------------

st.header("Subject Performance")

subject_data = pd.DataFrame({
    "Subject": ["Maths", "Reasoning", "Computer"],
    "Average Marks": [
        df["maths_marks"].mean(),
        df["reasoning_marks"].mean(),
        df["computer_marks"].mean()
    ]
})

st.bar_chart(
    subject_data.set_index("Subject")
)

# -----------------------------
# TOP PERFORMERS
# -----------------------------

st.header("Top 10 Performers")

top = (
    df.sort_values("nimcet_rank")
    .head(10)
)

st.dataframe(
    top[
        [
            "candidate_id",
            "study_hours_daily",
            "preparation_months",
            "mock_average_score",
            "nimcet_total_marks",
            "nimcet_rank"
        ]
    ],
    use_container_width=True
)

# -----------------------------
# ML MODEL INFORMATION
# -----------------------------

st.header("Machine Learning Model")

st.write("Random Forest Regression")

col1, col2 = st.columns(2)

col1.metric("Mean Absolute Error", "31.01")
col2.metric("R² Score", "0.82")

st.info(
    "The model predicts NIMCET total marks using study hours, "
    "preparation months, mock average score and subject-wise marks."
)