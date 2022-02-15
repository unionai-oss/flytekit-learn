import requests
import sys
from sklearn.datasets import load_breast_cancer

if __name__ == '__main__':
    # Assume the first parameter passed to the script is the gradio url produced as part of
    # setting up the ssh tunnel. For example, let's say the url returned by gradio is
    # https://12345.gradio.app, in this case we expect only the authority part (i.e. 12345.gradio.app)
    # to be passed in.
    # TODO: use a proper command-line parser like argv or click.
    gradio_url = sys.argv[1]

    breast_cancer_data = load_breast_cancer(as_frame=True)
    training_data = breast_cancer_data.frame
    features = training_data[breast_cancer_data.feature_names]

    metrics = requests.post(
        f"https://{gradio_url}/train?local=True",
        json={
            "hyperparameters": {"C": 1.0, "max_iter": 1000},
            "sample_frac": 1.0,
            "random_state": 123,
        },
    )
    print(f"Model: {metrics.text}")

    predictions = requests.post(
        f"https://{gradio_url}/predict?local=True&model_source=local",
        json={"inputs": {"sample_frac": 0.01, "random_state": 43}},
    )
    print(f"Predictions from dataset reader: {predictions.text}")

    predictions = requests.post(
        f"https://{gradio_url}/predict?local=True&model_source=local",
        json={"features": features.sample(10, random_state=42).to_dict(orient="records")},
    )
    print(f"Predictions from features: {predictions.text}")
