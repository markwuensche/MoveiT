# MoveiT

This project demonstrates a minimal pipeline for controlling a moving tunnel stimulus using EEG data. It consists of three components:

1. **EEG Classifier** (`eeg_classifier`): reads EEG data from an LSL stream (or generates random data if none is available) and classifies each sample as either `speed_up` or `slow_down`.
2. **Control Interface** (`interface`): converts classifier commands into a numerical speed value.
3. **Tunnel Display** (`tunnel_display`): renders a simple tunnel animation whose speed is controlled by the interface.

To start all components run:

```bash
python run_all.py
```

`run_all.py` launches the three modules as separate processes and passes data between them using multiprocessing queues.
