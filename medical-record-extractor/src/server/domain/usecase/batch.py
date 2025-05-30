import time
from threading import Lock

import schedule

from src.server.config.config import ApplicationConfig
from src.server.domain.port.ocr.iocrport import IOcrPort


class Batch:
    _self = None
    _lock = Lock()

    @classmethod
    def get_instance(cls):
        return Batch()

    def __new__(cls):
        if cls._self is None:
            with cls._lock:
                if cls._self is None:
                    cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        self._activation_time = ApplicationConfig.get_instance().get_batch_time()

    def start(self):
        print("[START] Batch thread started")
        schedule.every().day.at(self._activation_time).do(self._job)

        while 1:
            schedule.run_pending()
            time.sleep(1)

    @staticmethod
    def _job():
        IOcrPort().make_ocr()