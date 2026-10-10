import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# 1. Load data
df = pd.read_csv("data/processed/analytics_dataset.csv")

# 2. Select input features
features = [
    "study_hours_daily",
    "preparation_months",
    "mock_average_score",
    "maths_marks",
    "reasoning_marks",
    "computer_marks"
]

X = df[features]
y = df["nimcet_total_marks"]

# 3. Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Create and train Random Forest
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

print("Model trained successfully")

# 5. Make predictions
predictions = model.predict(X_test)

# 6. Evaluate model
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\nMean Absolute Error:", round(mae, 2))
print("R2 Score:", round(r2, 2))

# 7. Compare actual and predicted marks
results = pd.DataFrame({
    "Actual Marks": y_test.values,
    "Predicted Marks": predictions.round(2)
})

print("\nActual vs Predicted:")
print(results)