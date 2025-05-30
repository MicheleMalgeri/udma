from threading import Lock


class MDArchiveClient:
    _self = None
    _lock = Lock()

    @classmethod
    def get_instance(cls):
        return MDArchiveClient()

    def __new__(cls):
        if cls._self is None:
            with cls._lock:
                if cls._self is None:
                    cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        return
