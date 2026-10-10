import pandas as pd


# -----------------------------------
# 1. EXTRACT
# -----------------------------------

input_file = "data/raw/nimcet_data.csv"

df = pd.read_csv(input_file)

print("Dataset loaded successfully!")
print("Shape:", df.shape)


# -----------------------------------
# 2. INSPECT RAW DATA
# -----------------------------------

print("\nFirst 5 rows:")
print(df.head())

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)


# -----------------------------------
# 3. TRANSFORM
# -----------------------------------

def convert_social_media_hours(value):
    if value == "0-1":
        return 0.5
    elif value == "1-2":
        return 1.5
    elif value == "2-4":
        return 3.0
    else:
        return None


df["Social Media Hours"] = df[
    "Use of social media during preparation(hours);"
].apply(convert_social_media_hours)


print("\nSocial media transformation:")
print(
    df[
        [
            "Use of social media during preparation(hours);",
            "Social Media Hours"
        ]
    ].head(10)
)
# -----------------------------------
# 4. DATA QUALITY
# -----------------------------------

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nAge range:")
print("Minimum:", df["Age"].min())
print("Maximum:", df["Age"].max())

print("\nStudy hours range:")
print("Minimum:", df["Hours spend studying daily"].min())
print("Maximum:", df["Hours spend studying daily"].max())

print("\nPreparation months range:")
print("Minimum:", df["Months of Preparation"].min())
print("Maximum:", df["Months of Preparation"].max())

print("\nNIMCET total marks range:")
print("Minimum:", df["NIMCET Total Marks"].min())
print("Maximum:", df["NIMCET Total Marks"].max())

print("\nNIMCET rank range:")
print("Minimum:", df["NIMCET RANK"].min())
print("Maximum:", df["NIMCET RANK"].max())

# -----------------------------------
# 5. DATA QUALITY VALIDATION
# -----------------------------------

def run_data_quality_checks(df):

    dq_results = {}

    # Missing values
    dq_results["Missing Values"] = df.isnull().sum().sum()

    # Duplicate rows
    dq_results["Duplicate Rows"] = df.duplicated().sum()

    # Invalid age
    dq_results["Invalid Age"] = (
        ((df["Age"] < 15) | (df["Age"] > 60)).sum()
    )

    # Invalid study hours
    dq_results["Invalid Study Hours"] = (
        ((df["Hours spend studying daily"] < 0) |
         (df["Hours spend studying daily"] > 24)).sum()
    )

    # Invalid preparation months
    dq_results["Invalid Preparation Months"] = (
        ((df["Months of Preparation"] < 0) |
         (df["Months of Preparation"] > 120)).sum()
    )

    # Invalid NIMCET marks
    dq_results["Invalid NIMCET Marks"] = (
        (df["NIMCET Total Marks"] < 0).sum()
    )

    # Invalid rank
    dq_results["Invalid NIMCET Rank"] = (
        (df["NIMCET RANK"] <= 0).sum()
    )

    return dq_results


dq_report = run_data_quality_checks(df)

print("\nDATA QUALITY REPORT")
print("-------------------")

for check, count in dq_report.items():
    print(f"{check}: {count}")








total_errors = sum(dq_report.values())

if total_errors == 0:
    print("\nData Quality Status: PASSED")
else:
    print("\nData Quality Status: REVIEW REQUIRED")


# # -----------------------------------
# # 6. LOAD PROCESSED DATA
# # -----------------------------------

output_file = "data/processed/nimcet_cleaned.csv"

df.to_csv(output_file, index=False)

print(f"\nProcessed dataset saved to: {output_file}")