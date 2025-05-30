from threading import Lock

from minio import Minio

from src.server.config.config import ApplicationConfig


class MinioClient:
    _self = None
    _lock = Lock()

    @classmethod
    def get_instance(cls):
        return MinioClient()

    def __new__(cls):
        if cls._self is None:
            with cls._lock:
                if cls._self is None:
                    cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        self._config = ApplicationConfig.get_instance()
        self._client = self.create_client()

    def create_client(self):
        return Minio(self._config.get_minio_endpoint_url(),
                     access_key=self._config.get_minio_access_key(),
                     secret_key=self._config.get_minio_secret_key(),
                     secure=False)

    def get_client(self):
        return self._client
