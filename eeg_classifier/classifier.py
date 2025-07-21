import time
import os
import numpy as np
import cv2
from joblib import dump, load
from sklearn.linear_model import LogisticRegression


def collect_training_data(out_path="training_data.npz", n_samples=100):
    """Interactively collect training data from an EEG stream.

    Users label each sample as ``speed_up`` or ``slow_down`` by
    typing ``u`` or ``d``. If no LSL stream is available, random data is used.
    """
    inlet = None
    if LSL_AVAILABLE:
        try:
            print("Looking for an EEG stream...")
            streams = resolve_stream('type', 'EEG')
            inlet = StreamInlet(streams[0])
            print("EEG stream found")
        except Exception as exc:
            print(f"Could not connect to EEG stream ({exc}), using simulated data")
            inlet = None
    else:
        print("pylsl not available, using simulated data")

    rng = np.random.default_rng()
    samples = []
    labels = []

    print("Collecting training data. Press 'u' for speed_up, 'd' for slow_down.")
    for _ in range(n_samples):
        if inlet is not None:
            sample, _ = inlet.pull_sample(timeout=1.0)
            if sample is None:
                continue
            value = np.mean(sample)
        else:
            value = rng.random()

        label = input("Label [u/d]: ")
        label = 1 if label.lower().startswith('u') else 0
        samples.append([value])
        labels.append(label)

    np.savez(out_path, samples=np.array(samples), labels=np.array(labels))
    print(f"Saved training data to {out_path}")


def train_classifier(data_path="training_data.npz", model_path="model.joblib"):
    """Train a simple logistic regression model on collected data."""
    if not os.path.exists(data_path):
        raise FileNotFoundError(data_path)

    data = np.load(data_path)
    X = data["samples"]
    y = data["labels"]

    model = LogisticRegression()
    model.fit(X, y)
    dump(model, model_path)
    print(f"Model saved to {model_path}")

try:
    from pylsl import StreamInlet, resolve_stream
    LSL_AVAILABLE = True
except Exception:
    LSL_AVAILABLE = False


def run_classifier(out_queue, model_path="model.joblib", visualize=False):
    """Continuously read EEG data, classify, and send commands.

    Parameters
    ----------
    out_queue : multiprocessing.Queue
        Queue to send classification results ("speed_up" or "slow_down").
    """
    inlet = None
    if LSL_AVAILABLE:
        try:
            print("Looking for an EEG stream...")
            streams = resolve_stream('type', 'EEG')
            inlet = StreamInlet(streams[0])
            print("EEG stream found")
        except Exception as exc:
            print(f"Could not connect to EEG stream ({exc}), using simulated data")
            inlet = None
    else:
        print("pylsl not available, using simulated data")

    model = load(model_path) if os.path.exists(model_path) else None
    threshold = 0.5
    rng = np.random.default_rng()
    if visualize:
        cv2.namedWindow('Classifier', cv2.WINDOW_NORMAL)
        display = np.zeros((100, 300, 3), dtype=np.uint8)

    try:
        while True:
            if inlet is not None:
                sample, _ = inlet.pull_sample(timeout=1.0)
                if sample is None:
                    continue
                value = np.mean(sample)
            else:
                value = rng.random()

            if model is not None:
                pred = model.predict([[value]])[0]
                command = 'speed_up' if pred == 1 else 'slow_down'
            else:
                command = 'speed_up' if value > threshold else 'slow_down'

            if visualize:
                display[:] = 0
                color = (0, 255, 0) if command == 'speed_up' else (0, 0, 255)
                cv2.putText(display, command, (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 2)
                cv2.imshow('Classifier', display)
                cv2.waitKey(1)

            out_queue.put(command)
            time.sleep(0.1)
    finally:
        if visualize:
            cv2.destroyAllWindows()
