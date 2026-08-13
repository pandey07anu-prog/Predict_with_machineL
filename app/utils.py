from pathlib import Path

import joblib
import pandas as pd


# ==========================================
# Paths
# ==========================================

APP_DIR = Path(__file__).resolve().parent

MODEL_PATH = APP_DIR / "model.pkl"
TRANSFORMER_PATH = APP_DIR / "transformer.pkl"


# ==========================================
# Load model and transformer
# ==========================================

model = joblib.load(MODEL_PATH)
transformer = joblib.load(TRANSFORMER_PATH)


# ==========================================
# Features expected by the model
# ==========================================

FEATURE_COLUMNS = [
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
    "tenure_years",
    "spend_per_month"
]


# ==========================================
# Prepare customer data
# ==========================================

def prepare_customer(customer):
    """
    Convert one customer JSON object
    into a DataFrame expected by the model.
    """

    row = {}

    for column in FEATURE_COLUMNS:
        row[column] = customer.get(column, None)

    data = pd.DataFrame([row])

    # Convert TotalCharges to numeric
    data["TotalCharges"] = pd.to_numeric(
        data["TotalCharges"],
        errors="coerce"
    )

    # Convert numerical columns to numeric
    data["SeniorCitizen"] = pd.to_numeric(
        data["SeniorCitizen"],
        errors="coerce"
    )

    data["tenure"] = pd.to_numeric(
        data["tenure"],
        errors="coerce"
    )

    data["MonthlyCharges"] = pd.to_numeric(
        data["MonthlyCharges"],
        errors="coerce"
    )

    data["tenure_years"] = pd.to_numeric(
        data["tenure_years"],
        errors="coerce"
    )

    data["spend_per_month"] = pd.to_numeric(
        data["spend_per_month"],
        errors="coerce"
    )

    return data


# ==========================================
# Prediction
# ==========================================

def predict_customer(customer):
    """
    Generate churn probability and prediction
    for one customer.
    """

    data = prepare_customer(customer)

    transformed_data = transformer.transform(data)

    probability = float(
        model.predict_proba(transformed_data)[0, 1]
    )

    if probability >= 0.5:
        prediction = "Yes"
    else:
        prediction = "No"

    return probability, prediction