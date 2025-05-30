from threading import Lock

from pymongo import MongoClient

from src.server.config.config import ApplicationConfig


class MongoDBClient:
    _config: ApplicationConfig
    _self = None
    _lock = Lock()
    _client = None

    @staticmethod
    def get_instance():
        return MongoDBClient()

    def __new__(cls):
        if cls._self is None:
            with cls._lock:
                if cls._self is None:
                    cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        self._config = ApplicationConfig.get_instance()
        self.set_client()

    def get_client(self):
        return self._client

    def set_client(self):
        self._client = MongoClient(self._config.get_mongo_db_host(), int(self._config.get_mongo_db_port()), document_class=dict, connect=True, username=self._config.get_mongo_db_username(), password=self._config.get_mongo_db_password())

    def check_connection(self) -> bool:
        return self._client.ping()
