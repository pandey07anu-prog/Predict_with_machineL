from flask import Flask, jsonify, request
from .utils import predict_customer

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({
        "status": "ok"
    })


@app.post("/predict")
def predict():
    try:
        payload = request.get_json(silent=True)

        if not payload or "customer" not in payload:
            return jsonify({
                "error": "Request must contain a 'customer' JSON object."
            }), 400

        probability, prediction = predict_customer(
            payload["customer"]
        )

        return jsonify({
            "churn_probability": round(float(probability), 6),
            "churn_prediction": prediction
        })

    except Exception as exc:
        app.logger.exception("Prediction failed")

        return jsonify({
            "error": str(exc)
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8000,
        debug=False
    )