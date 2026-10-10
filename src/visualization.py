import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. CONNECT TO MYSQL
# ==========================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dhir#2004",
    database="nimcet_analytics"
)

print("Connected to MySQL")


# ==========================================
# 2. LOAD DATA
# ==========================================

query = """
SELECT
    c.study_hours_daily,
    c.preparation_months,
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

print("Dataset loaded:", df.shape)


# ==========================================
# 3. CORRELATION HEATMAP
# ==========================================

correlation = df.corr()

plt.figure(figsize=(10, 7))
plt.imshow(correlation, cmap="coolwarm")
plt.colorbar()

plt.xticks(range(len(correlation.columns)),
           correlation.columns, rotation=90)
plt.yticks(range(len(correlation.columns)),
           correlation.columns)

plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()


# ==========================================
# 4. MOCK SCORE vs NIMCET MARKS
# ==========================================

plt.scatter(
    df["mock_average_score"],
    df["nimcet_total_marks"]
)

plt.xlabel("Average Mock Score")
plt.ylabel("NIMCET Total Marks")
plt.title("Mock Score vs NIMCET Marks")
plt.show()


# ==========================================
# 5. PREPARATION MONTHS vs NIMCET MARKS
# ==========================================

plt.scatter(
    df["preparation_months"],
    df["nimcet_total_marks"]
)

plt.xlabel("Preparation Months")
plt.ylabel("NIMCET Total Marks")
plt.title("Preparation Duration vs NIMCET Marks")
plt.show()


# ==========================================
# 6. STUDY HOURS vs NIMCET MARKS
# ==========================================

plt.scatter(
    df["study_hours_daily"],
    df["nimcet_total_marks"]
)

plt.xlabel("Daily Study Hours")
plt.ylabel("NIMCET Total Marks")
plt.title("Study Hours vs NIMCET Marks")
plt.show()


# ==========================================
# 7. SUBJECT PERFORMANCE
# ==========================================

subjects = ["Maths", "Reasoning", "Computer"]

average_marks = [
    df["maths_marks"].mean(),
    df["reasoning_marks"].mean(),
    df["computer_marks"].mean()
]

plt.bar(subjects, average_marks)

plt.xlabel("Subject")
plt.ylabel("Average Marks")
plt.title("Average Subject Performance")
plt.show()

# ==========================================
# Maths Marks vs NIMCET Marks
plt.figure(figsize=(8, 6))

plt.scatter(df["maths_marks"], df["nimcet_total_marks"])

plt.title("Maths Marks vs NIMCET Marks")
plt.xlabel("Maths Marks")
plt.ylabel("NIMCET Total Marks")

plt.show()

# ==========================================
# 8. CLOSE CONNECTION
# ==========================================

conn.close()

print("Visualization completed successfully!")