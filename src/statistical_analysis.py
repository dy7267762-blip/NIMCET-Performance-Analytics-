import pandas as pd
import mysql.connector

# ==============================
# 1. CONNECT TO MYSQL
# ==============================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dhir#2004",          
    database="nimcet_analytics"
)

print("Connected to MySQL")


# ==============================
# 2. LOAD ANALYTICAL DATA
# ==============================

query = """
SELECT
    c.candidate_id,
    c.age,
    c.gender,
    c.study_hours_daily,
    c.preparation_months,
    c.jee_prepared,
    c.is_dropper,
    ep.mock_average_score,
    ep.mock_tests_count,
    ep.maths_marks,
    ep.reasoning_marks,
    ep.computer_marks,
    ep.nimcet_total_marks,
    ep.nimcet_rank
FROM candidates c
JOIN exam_performance ep
    ON c.candidate_id = ep.candidate_id
"""

df = pd.read_sql(query, conn)

print("\nDataset loaded")
print("Shape:", df.shape)

print("\nFirst 5 rows:")
print(df.head())


# ==============================
# 3. BASIC STATISTICS
# ==============================

print("\n" + "=" * 50)
print("DESCRIPTIVE STATISTICS")
print("=" * 50)

print(df.describe())


# ==============================
# 4. CORRELATION ANALYSIS
# ==============================

print("\n" + "=" * 50)
print("CORRELATION WITH NIMCET TOTAL MARKS")
print("=" * 50)

# Remove ID columns because they are not analytical features
correlation_df = df.drop(columns=["candidate_id"], errors="ignore")

correlation = (
    correlation_df
    .corr(numeric_only=True)["nimcet_total_marks"]
    .sort_values(ascending=False)
)

print(correlation)

# ==============================
# 5. STUDY HOURS ANALYSIS
# ==============================

print("\n" + "=" * 50)
print("STUDY HOURS ANALYSIS")
print("=" * 50)

study_analysis = (
    df.groupby("study_hours_daily")
      .agg(
          candidates=("candidate_id", "count"),
          avg_marks=("nimcet_total_marks", "mean"),
          avg_rank=("nimcet_rank", "mean")
      )
      .round(2)
)

print(study_analysis)


# ==============================
# 6. PREPARATION MONTHS ANALYSIS
# ==============================

print("\n" + "=" * 50)
print("PREPARATION MONTHS ANALYSIS")
print("=" * 50)

preparation_analysis = (
    df.groupby("preparation_months")
      .agg(
          candidates=("candidate_id", "count"),
          avg_marks=("nimcet_total_marks", "mean"),
          avg_rank=("nimcet_rank", "mean")
      )
      .round(2)
)

print(preparation_analysis)


# ==============================
# 7. MOCK TEST ANALYSIS
# ==============================

print("\n" + "=" * 50)
print("MOCK TEST ANALYSIS")
print("=" * 50)

mock_analysis = (
    df.groupby("mock_tests_count")
      .agg(
          candidates=("candidate_id", "count"),
          avg_mock_score=("mock_average_score", "mean"),
          avg_marks=("nimcet_total_marks", "mean"),
          avg_rank=("nimcet_rank", "mean")
      )
      .round(2)
)

print(mock_analysis)


# ==============================
# 8. SUBJECT PERFORMANCE
# ==============================

print("\n" + "=" * 50)
print("SUBJECT PERFORMANCE")
print("=" * 50)

subjects = {
    "Maths": df["maths_marks"].mean(),
    "Reasoning": df["reasoning_marks"].mean(),
    "Computer": df["computer_marks"].mean()
}

for subject, average in subjects.items():
    print(f"{subject}: {average:.2f}")


# ==============================
# 9. TOP PERFORMERS
# ==============================

print("\n" + "=" * 50)
print("TOP 10 PERFORMERS")
print("=" * 50)

top_performers = (
    df.sort_values("nimcet_rank")
      .head(10)
)

print(
    top_performers[
        [
            "candidate_id",
            "study_hours_daily",
            "preparation_months",
            "mock_average_score",
            "nimcet_total_marks",
            "nimcet_rank"
        ]
    ]
)


# ==============================
# 10. SAVE ANALYTICAL DATA
# ==============================

df.to_csv(
    "data/processed/analytics_dataset.csv",
    index=False
)

print("\nAnalytics dataset saved successfully.")

conn.close()

print("MySQL connection closed.")