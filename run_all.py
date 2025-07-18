from multiprocessing import Process
from eeg_classifier.classifier import run_classifier
from interface.control_interface import run_interface
from tunnel_display.run_display import run_display

if __name__ == "__main__":
    Process(target=run_classifier).start()
    Process(target=run_interface).start()
    Process(target=run_display).start()
