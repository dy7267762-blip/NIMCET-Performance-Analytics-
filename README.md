# NIMCET Performance Analysis & Marks Prediction

A data analytics and machine learning project that analyzes NIMCET candidate data to explore patterns associated with exam performance and estimate total marks using a Random Forest regression model. The project combines Python, Pandas, MySQL, scikit-learn, and Streamlit.

## Project Objectives

- Clean, transform, and validate candidate data through an ETL pipeline.
- Analyze numerical variables and performance patterns.
- Use SQL and Pandas for descriptive and group-wise analysis.
- Examine relationships between candidate features, subject marks, total marks, and rank.
- Train a regression model to estimate NIMCET total marks.
- Present analysis and predictions through an interactive dashboard.

## Tech Stack

- **Python** — data processing and analysis
- **Pandas / NumPy** — data cleaning, transformation, and statistics
- **MySQL** — structured storage and SQL queries
- **scikit-learn** — Random Forest regression and model evaluation
- **Matplotlib / Seaborn** — visualizations, including correlation heatmaps
- **Streamlit** — interactive dashboard

## Project Workflow

```text
Candidate Data
     |
     v
ETL Pipeline (Python + Pandas)
     |
     v
Processed / Validated Dataset
     |
     v
MySQL Storage and SQL Analysis
     |
     v
Statistical Analysis
(descriptive statistics, correlation, group-wise analysis)
     |
     v
Random Forest Regression
     |
     v
Model Evaluation (MAE and R²)
     |
     v
Streamlit Dashboard
```

## Analysis Performed

### 1. Data Preparation (ETL)

The ETL workflow prepares raw candidate data for analysis. It includes checks such as data-type validation, missing-value checks, duplicate checks, and transformations needed to make the data usable.

### 2. SQL and Statistical Analysis

The analytical dataset is loaded from MySQL by joining the `candidates` and `exam_performance` tables on `candidate_id`.

The analysis includes:

- Descriptive statistics such as count, mean, standard deviation, quartiles, minimum, and maximum.
- Correlation analysis between numerical variables.
- Group-wise comparisons based on daily study hours, preparation months, and number of mock tests.
- Average marks and rank comparisons across groups.
- Average subject marks for Maths, Reasoning, and Computer.
- Inspection of the top performers by rank.

### 3. Correlation Heatmap

A correlation heatmap helps visualize the strength and direction of linear relationships between numerical variables. In the analyzed dataset, examples included:

- Maths marks and total marks: approximately **0.87**
- Mock average score and total marks: approximately **0.72**
- Preparation months and total marks: approximately **0.51**
- Rank and total marks: approximately **-0.75**

Correlation indicates association, not causation. These values describe the analyzed dataset and should not be interpreted as proof that one factor causes better performance.

## Machine Learning

A `RandomForestRegressor` from scikit-learn is trained to estimate `nimcet_total_marks`.

### Input Features

- `study_hours_daily`
- `preparation_months`
- `mock_average_score`
- `maths_marks`
- `reasoning_marks`
- `computer_marks`

### Target

- `nimcet_total_marks`

### Training Setup

- Train/test split: **80% training / 20% testing**
- Number of trees: **100**
- `random_state`: **42**

### Reported Evaluation Results

| Metric | Result | Interpretation |
|---|---:|---|
| Mean Absolute Error (MAE) | 31.01 | Predictions differed from actual marks by about 31 marks on average on the test set. |
| R² score | 0.82 | The model explained approximately 82% of the variation in total marks on the test set. |

These are the reported results from the current model run; results can vary if the dataset or model configuration changes. R² is not the same as classification accuracy.

### Important Modeling Limitation

The current model includes Maths, Reasoning, and Computer marks as input features, while predicting total marks. Since subject marks may contribute directly to the total, this can make prediction easier and may cause target leakage depending on the intended use case. This model is therefore not a strict pre-exam prediction model. To estimate marks before the exam, train and evaluate a separate model using only features available before the exam, such as preparation duration, study hours, and mock-test performance.

## Repository Structure

The following is an illustrative structure; adjust paths and filenames to match the actual repository.

```text
NIMCET-Performance-Analysis/
├── data/
│   └── processed/
│       └── analytics_dataset.csv
├── src/
│   ├── etl.py
│   ├── statistical_analysis.py
│   └── machine_learning.py
├── app.py
├── requirements.txt
└── README.md
```

## Setup and Usage

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd NIMCET-Performance-Analysis
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

If the repository contains `requirements.txt`:

```bash
pip install -r requirements.txt
```

Otherwise, install the core libraries:

```bash
pip install pandas numpy scikit-learn mysql-connector-python streamlit matplotlib seaborn
```

### 4. Configure MySQL

Create the `nimcet_analytics` database and configure the `candidates` and `exam_performance` tables according to the schema used by the project. Update the connection settings in the script or, preferably, load credentials from environment variables.

**Security:** Do not commit database passwords, API keys, or other secrets to GitHub. If credentials have already been committed, rotate them and remove them from the repository history where appropriate.

### 5. Run the analysis scripts

Use the actual paths in your repository. For example:

```bash
python src/etl.py
python src/statistical_analysis.py
python src/machine_learning.py
```

The statistical analysis script reads from MySQL and saves an analytical CSV to `data/processed/analytics_dataset.csv`. The machine learning script expects that CSV to exist.

### 6. Launch the Streamlit dashboard

If your dashboard entry file is `app.py`, run:

```bash
streamlit run app.py
```

If the dashboard has a different filename, replace `app.py` with that filename.

## Interpretation and Limitations

- The dataset contains just over 100 records, so results may not generalize to all NIMCET candidates.
- Correlation does not establish causation.
- MAE and R² evaluate performance on the held-out test split; they do not guarantee the same performance on new data.
- A larger dataset, cross-validation, model comparison, and carefully selected pre-exam features would help strengthen the evaluation.

## Future Improvements

- Collect a larger and more representative dataset.
- Use cross-validation and compare multiple regression algorithms.
- Tune model hyperparameters using a documented validation procedure.
- Build a separate pre-exam model that excludes actual exam subject marks.
- Add clearer dashboard explanations, feature comparisons, and model evaluation visuals.
- Deploy the dashboard for wider access.

## Disclaimer

This project is intended for educational and analytical purposes. Its findings describe the dataset used and should not be treated as definitive advice about how any individual candidate will perform.
