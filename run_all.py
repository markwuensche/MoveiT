from multiprocessing import Process, Queue
from eeg_classifier.classifier import run_classifier
from interface.control_interface import run_interface
from tunnel_display.run_display import run_display

if __name__ == "__main__":
    classifier_queue = Queue()
    speed_queue = Queue()
    Process(target=run_classifier, args=(classifier_queue,)).start()
    Process(target=run_interface, args=(classifier_queue, speed_queue)).start()
    Process(target=run_display, args=(speed_queue,)).start()
