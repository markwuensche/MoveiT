# MoveiT

This project demonstrates a minimal pipeline for controlling a moving tunnel stimulus using EEG data. It consists of three components:

1. **EEG Classifier** (`eeg_classifier`): reads EEG data from an LSL stream (or generates random data if none is available) and classifies each sample as either `speed_up` or `slow_down`. The classifier can be trained on recorded data using the provided helper functions.
2. **Control Interface** (`interface`): converts classifier commands into a numerical speed value.

3. **Tunnel Display** (`tunnel_display`): shows an OpenGL tunnel stimulus from
   `tunnel_module.py` whose speed is controlled by the interface.

To start all components run:

```bash
python run_all.py
```

`run_all.py` launches the three modules as separate processes and passes data between them using multiprocessing queues.

Press `q` in the tunnel window to exit the demo.

## Training the classifier

Run `collect_training_data()` from `eeg_classifier.classifier` to record labeled
EEG samples. Afterwards call `train_classifier()` to create a `model.joblib`
file. When present, this model is loaded automatically by `run_classifier`. If
`run_all.py` is executed, classifier decisions will be displayed in a small
window in real time.

If OpenCV cannot create or display GUI windows (e.g. on a headless server),
the classifier falls back to printing the decisions in the terminal so you can
still observe the output.

