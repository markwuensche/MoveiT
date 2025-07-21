import time
import numpy as np
try:
    from pylsl import StreamInlet, resolve_stream
    LSL_AVAILABLE = True
except Exception:
    LSL_AVAILABLE = False


def run_classifier(out_queue):
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

    threshold = 0.5
    rng = np.random.default_rng()

    while True:
        if inlet is not None:
            sample, _ = inlet.pull_sample(timeout=1.0)
            if sample is None:
                continue
            value = np.mean(sample)
        else:
            value = rng.random()

        command = 'speed_up' if value > threshold else 'slow_down'
        out_queue.put(command)
        time.sleep(0.1)
