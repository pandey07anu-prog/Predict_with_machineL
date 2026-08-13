# Customer Churn Prediction Deployment

## Project Overview

This project deploys a Customer Churn Prediction machine learning model as a Flask REST API and provides a batch-scoring workflow.

The system supports real-time prediction for individual customers through an HTTP API and automatic batch scoring for multiple customers.

## Project Architecture

```text
Customer Data
     |
     v
Preprocessing Transformer
     |
     v
Trained Churn Model
     |
     +-------------------+
     |                   |
     v                   v
 Flask API          Batch Pipeline
     |                   |
 /predict                |
     |                   |
     +---------+---------+
               |
               v
       Prediction Results
               |
               v
       Monitoring Logs
```

## Project Structure

```text
customer-churn-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── model.pkl
│   ├── transformer.pkl
│   └── utils.py
│
├── test_data/
│   ├── sample_input.json
│   └── all_customers.csv
│
├── logs/
│   └── batch_log.txt
│
├── batch.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Technologies Used

* Python
* Flask
* Pandas
* NumPy
* Scikit-learn
* Joblib
* Requests
* REST API
* Machine Learning

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```powershell
pip install -r requirements.txt
```

## Running the API

From the project root directory, run:

```powershell
python -m app.main
```

The Flask API runs on:

```text
http://127.0.0.1:8000
```

The application provides the following endpoints:

```text
GET  /health
POST /predict
```

## Health Check

To verify that the API is running:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

A successful response confirms that the API is available.

## Real-Time Prediction

The prediction endpoint is:

```text
POST /predict
```

The API accepts customer information as JSON.

A sample request is provided in:

```text
test_data/sample_input.json
```

Example PowerShell request:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/predict `
  -Method POST `
  -ContentType "application/json" `
  -InFile "test_data/sample_input.json"
```

Example response:

```json
{
    "churn_prediction": "Yes",
    "churn_probability": 0.641994
}
```

The API converts the incoming customer JSON into a pandas DataFrame, applies the saved preprocessing transformer, and sends the transformed data to the trained machine learning model.

## Batch Scoring

The batch pipeline scores multiple customers through the Flask API.

Input file:

```text
test_data/all_customers.csv
```

Run the batch pipeline with:

```powershell
python batch.py --input test_data/all_customers.csv
```

The script:

1. Reads the customer CSV file.
2. Sends each customer to the `/predict` endpoint.
3. Collects the prediction and churn probability.
4. Records failed requests.
5. Calculates the average churn probability.
6. Saves the results to `scored_customers.csv`.
7. Records batch execution information in `logs/batch_log.txt`.

Example successful execution:

```text
Customers: 100
Failures: 0
Average churn probability: 0.2702
Saved: scored_customers.csv
```

## Logging and Monitoring

Batch execution logs are stored in:

```text
logs/batch_log.txt
```

The logging system records:

* Total number of customers processed
* Failed predictions
* Average churn probability
* Average API response time
* Execution timestamps
* Errors encountered during processing

These metrics can be reviewed regularly to identify failures or changes in model behavior.

## Model Artifacts

The trained machine learning model is stored in:

```text
app/model.pkl
```

The preprocessing pipeline is stored in:

```text
app/transformer.pkl
```

The preprocessing transformer is saved separately so that incoming API data is transformed consistently with the data used during model training.

## Retraining Strategy

The churn model should be reviewed regularly and retrained when sufficient new labeled customer data becomes available.

Retraining should also be considered when model performance decreases, customer behavior changes, data drift is detected, or business conditions change significantly.

The retraining process should include collecting updated data, applying the same preprocessing methodology, training and evaluating the model, comparing it with the existing production model, and replacing the model artifact only if the new model meets the required performance criteria.

Model evaluation should include appropriate classification metrics such as accuracy, precision, recall, F1-score, ROC-AUC, and confusion matrix analysis.

## Drift Detection

Data and model behavior should be monitored after deployment.

Data drift can be detected by comparing the distribution of important input features in new customer data with the original training data. Changes in categorical distributions, numerical statistics, and missing-value rates can be monitored.

Prediction drift can also be monitored by tracking changes in churn probabilities and predicted churn rates over time.

If significant drift is detected, the underlying customer behavior and data quality should be investigated. If necessary, the model should be retrained using more recent labeled data.

## Versioning Strategy

The model and preprocessing pipeline should be versioned together because the model depends on the exact preprocessing used during training.

Each production release should have a unique version identifier, for example:

```text
model_v1
model_v2
model_v3
```

The corresponding preprocessing transformer should use the same version.

Changes to model code, preprocessing code, dependencies, and configuration should be tracked using Git. Previous model versions should be retained so that a previous stable version can be restored if a new model performs poorly after deployment.

## Production Workflow

The intended workflow is:

```text
Customer Data
     |
     v
Validation
     |
     v
Preprocessing
     |
     v
Churn Model
     |
     v
Prediction
     |
     v
Logging
     |
     v
Monitoring
     |
     v
Retraining when required
```

The Flask API supports real-time customer predictions, while the batch pipeline supports automated scoring of multiple customers.

## .gitignore

The repository excludes local and generated Python environment files such as:

```text
.venv/
__pycache__/
*.py[cod]
.env
.DS_Store
```

This prevents unnecessary local environment files from being committed to the repository.

## Conclusion

This project demonstrates an end-to-end machine learning deployment workflow, including:

* Customer churn model training
* Model persistence
* Preprocessing pipeline persistence
* Flask REST API
* Real-time inference
* Batch inference
* Logging
* Monitoring
* Model retraining strategy
* Data drift detection
* Model and pipeline versioning

The project converts a trained Customer Churn Prediction model into a reusable production-style prediction system.# Predict_with_machineL
