import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# ==========================================
# 1. Load dataset
# ==========================================

df = pd.read_csv("gold_churn_data.csv")


# ==========================================
# 2. Create X and y
# ==========================================

X = df.drop("Churn", axis=1)

y = df["Churn"].map({
    "Yes": 1,
    "No": 0
})


# ==========================================
# 3. Remove columns not used by the model
# ==========================================

X = X.drop(
    columns=["customerID", "Unnamed: 0"],
    errors="ignore"
)


# ==========================================
# 4. Convert TotalCharges to numeric
# ==========================================

X["TotalCharges"] = pd.to_numeric(
    X["TotalCharges"],
    errors="coerce"
)


# ==========================================
# 5. Identify categorical and numerical columns
# ==========================================

categorical_cols = X.select_dtypes(
    include=["object"]
).columns.tolist()

numerical_cols = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()


print("Categorical columns:")
print(categorical_cols)

print("\nNumerical columns:")
print(numerical_cols)


# ==========================================
# 6. Create preprocessing pipeline
# ==========================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            SimpleImputer(strategy="mean"),
            numerical_cols
        ),
        (
            "cat",
            Pipeline([
                (
                    "imputer",
                    SimpleImputer(strategy="most_frequent")
                ),
                (
                    "onehot",
                    OneHotEncoder(
                        handle_unknown="ignore",
                        sparse_output=False
                    )
                )
            ]),
            categorical_cols
        )
    ]
)


# ==========================================
# 7. Fit preprocessing pipeline
# ==========================================

X_transformed = preprocessor.fit_transform(X)


# ==========================================
# 8. Train Logistic Regression model
# ==========================================

model = LogisticRegression(
    max_iter=2000,
    random_state=42
)

model.fit(
    X_transformed,
    y
)


# ==========================================
# 9. Save model and transformer
# ==========================================

joblib.dump(
    model,
    "app/model.pkl"
)

joblib.dump(
    preprocessor,
    "app/transformer.pkl"
)


# ==========================================
# 10. Print information
# ==========================================

print("\n========================================")
print("Model trained successfully!")
print("========================================")
print("Model saved to: app/model.pkl")
print("Transformer saved to: app/transformer.pkl")
print("Training rows:", len(X))
print("Features after preprocessing:", X_transformed.shape[1])
print("========================================")