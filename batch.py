import logging
import time
from pathlib import Path

import pandas as pd
import requests


API_URL = "http://127.0.0.1:8000/predict"

INPUT_FILE = "test_data/all_customers.csv"
OUTPUT_FILE = "scored_customers.csv"

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "batch_log.txt",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def main():

    print("Starting batch scoring...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Customers found: {len(df)}")

    probabilities = []
    predictions = []

    failures = 0
    response_times = []

    for index, row in df.iterrows():

        print(f"Processing customer {index + 1}/{len(df)}")

        customer = row.to_dict()

        customer.pop("Churn", None)
        customer.pop("customerID", None)
        customer.pop("Unnamed: 0", None)

        start = time.perf_counter()

        try:

            response = requests.post(
                API_URL,
                json={"customer": customer},
                timeout=10
            )

            elapsed = time.perf_counter() - start

            response_times.append(elapsed)

            if response.status_code != 200:

                print(
                    f"ERROR customer {index + 1}: "
                    f"HTTP {response.status_code}"
                )

                probabilities.append(None)
                predictions.append(None)

                failures += 1

                continue

            result = response.json()

            probabilities.append(
                result["churn_probability"]
            )

            predictions.append(
                result["churn_prediction"]
            )

        except Exception as error:

            print(
                f"ERROR customer {index + 1}: {error}"
            )

            probabilities.append(None)
            predictions.append(None)

            failures += 1

            logging.exception(
                "Customer %s failed",
                index + 1
            )

    df["churn_probability"] = probabilities
    df["churn_prediction"] = predictions

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    valid_probabilities = [
        x for x in probabilities
        if x is not None
    ]

    if valid_probabilities:

        average_probability = (
            sum(valid_probabilities)
            / len(valid_probabilities)
        )

    else:

        average_probability = 0

    if response_times:

        average_response_time = (
            sum(response_times)
            / len(response_times)
            * 1000
        )

    else:

        average_response_time = 0

    logging.info(
        "Total customers: %s",
        len(df)
    )

    logging.info(
        "Failures: %s",
        failures
    )

    logging.info(
        "Average churn probability: %.4f",
        average_probability
    )

    logging.info(
        "Average API response time: %.2f ms",
        average_response_time
    )

    print()
    print("================================")
    print("BATCH SCORING COMPLETED")
    print("================================")
    print(f"Customers: {len(df)}")
    print(f"Failures: {failures}")
    print(
        f"Average churn probability: "
        f"{average_probability:.4f}"
    )
    print(
        f"Average response time: "
        f"{average_response_time:.2f} ms"
    )
    print(f"Saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()