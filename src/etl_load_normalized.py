import os
import pandas as pd
import mysql.connector


# =========================================
# CONFIGURATION
# =========================================

CSV_PATH = "data/processed/nimcet_cleaned.csv"

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "Dhir#2004"),
    "database": os.getenv("DB_NAME", "nimcet_analytics"),
}


# =========================================
# COLLEGE TYPE MAPPING
# =========================================

COLLEGE_TYPE_MAP = {
    "Other Government College": "Other Government",
    "Other Private College": "Other Private",
    "Dropped": "Not Applicable",
}


# =========================================
# GET OR CREATE LOOKUP VALUE
# =========================================

def get_or_create(cursor, table, id_col, name_col, name, extra_cols=None):

    cursor.execute(
        f"SELECT {id_col} FROM {table} WHERE {name_col} = %s",
        (name,)
    )

    row = cursor.fetchone()

    if row:
        return row[0]

    cols = [name_col] + list((extra_cols or {}).keys())
    vals = [name] + list((extra_cols or {}).values())

    placeholders = ", ".join(["%s"] * len(vals))

    cursor.execute(
        f"""
        INSERT INTO {table}
        ({', '.join(cols)})
        VALUES ({placeholders})
        """,
        vals
    )

    return cursor.lastrowid


# =========================================
# MAIN ETL FUNCTION
# =========================================

def main():

    print("Starting ETL process...")

    # -------------------------------------
    # 1. READ CSV
    # -------------------------------------

    df = pd.read_csv(CSV_PATH)

    df.columns = [c.strip() for c in df.columns]

    print(f"Dataset loaded: {len(df)} rows")


    # -------------------------------------
    # 2. CONNECT TO MYSQL
    # -------------------------------------

    conn = mysql.connector.connect(**DB_CONFIG)

    cur = conn.cursor()

    print("Connected to MySQL")


    # -------------------------------------
    # 3. LOAD LOOKUP TABLES
    # -------------------------------------

    def load_map(table, id_col, name_col):

        cur.execute(
            f"SELECT {name_col}, {id_col} FROM {table}"
        )

        return {
            name: _id
            for name, _id in cur.fetchall()
        }


    category_map = load_map(
        "categories",
        "category_id",
        "category_name"
    )

    stream_map = load_map(
        "graduation_streams",
        "stream_id",
        "stream_name"
    )

    band_map = load_map(
        "social_media_usage_bands",
        "band_id",
        "band_label"
    )

    difficulty_map = load_map(
        "difficulty_levels",
        "difficulty_id",
        "difficulty_name"
    )

    college_map = load_map(
        "colleges",
        "college_id",
        "college_name"
    )


    # -------------------------------------
    # 4. PROCESS EACH CANDIDATE
    # -------------------------------------

    inserted = 0

    for _, row in df.iterrows():

        # =================================
        # COLLEGE
        # =================================

        college_name = str(
            row["College you are currently in"]
        ).strip()

        if college_name not in college_map:

            college_type = COLLEGE_TYPE_MAP.get(
                college_name,
                "NIT"
            )

            college_map[college_name] = get_or_create(
                cur,
                "colleges",
                "college_id",
                "college_name",
                college_name,
                {
                    "college_type": college_type
                }
            )


        # =================================
        # CANDIDATE
        # =================================

        cur.execute(
            """
            INSERT INTO candidates (
                response_timestamp,
                age,
                gender,
                preferred_study_time,
                jee_prepared,
                study_hours_daily,
                preparation_months,
                background_12th,
                social_media_band_id,
                category_id,
                college_id,
                graduation_stream_id,
                is_dropper
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
            )
            """,
            (
                row["Timestamp"],
                int(row["Age"]),
                str(row["Gender"]).strip(),
                str(
                    row["Preferred time of Study"]
                ).strip(),

                str(
                    row[
                        "Have you prepared for JEE "
                        "(Joint Enterance Examination)"
                    ]
                ).strip().upper() == "YES",

                float(
                    row["Hours spend studying daily"]
                ),

                int(
                    row["Months of Preparation"]
                ),

                str(
                    row["12th Background"]
                ).strip(),

                band_map[
                    str(
                        row[
                            "Use of social media during preparation(hours);"
                        ]
                    ).strip()
                ],

                category_map[
                    str(row["Category"]).strip()
                ],

                college_map[college_name],

                stream_map[
                    str(
                        row["Graduation Stream"]
                    ).strip()
                ],

                str(
                    row["Dropper?"]
                ).strip().upper() == "YES"
            )
        )

        candidate_id = cur.lastrowid


        # =================================
        # STUDY MODES
        # =================================

        modes = str(
            row["Mode of Study"]
        ).split(",")

        for mode in modes:

            mode = mode.strip()

            if not mode:
                continue

            mode_id = get_or_create(
                cur,
                "study_modes",
                "mode_id",
                "mode_name",
                mode
            )

            cur.execute(
                """
                INSERT IGNORE INTO candidate_study_modes
                (candidate_id, mode_id)
                VALUES (%s, %s)
                """,
                (
                    candidate_id,
                    mode_id
                )
            )


        # =================================
        # PREPARATION ISSUES
        # =================================

        issues_raw = row[
            "Issues faced during preparation"
        ]

        if isinstance(issues_raw, str):

            issues = issues_raw.split(",")

            for issue in issues:

                issue = issue.strip()

                if not issue:
                    continue

                issue_id = get_or_create(
                    cur,
                    "preparation_issues",
                    "issue_id",
                    "issue_name",
                    issue
                )

                cur.execute(
                    """
                    INSERT IGNORE INTO
                    candidate_preparation_issues
                    (candidate_id, issue_id)
                    VALUES (%s, %s)
                    """,
                    (
                        candidate_id,
                        issue_id
                    )
                )


        # =================================
        # EXAM PERFORMANCE
        # =================================

        cur.execute(
            """
            INSERT INTO exam_performance (
                candidate_id,
                mock_average_score,
                mock_tests_count,
                maths_marks,
                reasoning_marks,
                computer_marks,
                nimcet_total_marks,
                nimcet_rank,
                difficulty_id
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            """,
            (
                candidate_id,

                int(
                    row["Mock test average score"]
                ),

                int(
                    row["Number of mock tests given?"]
                ),

                float(
                    row["NIMCET Maths Marks"]
                ),

                float(
                    row["NIMCET Reasoning Marks"]
                ),

                float(
                    row["NIMCET Computer Marks"]
                ),

                float(
                    row["NIMCET Total Marks"]
                ),

                int(
                    row["NIMCET RANK"]
                ),

                difficulty_map[
                    str(
                        row["Difficulty of paper"]
                    ).strip()
                ]
            )
        )


        inserted += 1


    # -------------------------------------
    # 5. COMMIT
    # -------------------------------------

    conn.commit()

    print()
    print("=" * 50)
    print(f"ETL COMPLETED SUCCESSFULLY")
    print(f"Candidates inserted: {inserted}")
    print("=" * 50)


    # -------------------------------------
    # 6. CLOSE CONNECTION
    # -------------------------------------

    cur.close()
    conn.close()


# =========================================
# PROGRAM ENTRY
# =========================================

if __name__ == "__main__":
    main()