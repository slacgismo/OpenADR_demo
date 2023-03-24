import time
import threading


class ProcessThread(threading.Thread):
    def __init__(self, target):
        super(ProcessThread, self).__init__()
        self.target = target
        self._stop_event = threading.Event()

    def run(self):
        self.target()

    def stop(self):
        self._stop_event.set()
