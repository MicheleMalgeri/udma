import io
from threading import Lock

from src.server.adapter.minio.client import MinioClient
from src.server.config.config import ApplicationConfig
from src.server.domain.port.s3.simple_storage_port import SimpleStoragePort


class MinioService(SimpleStoragePort):
    _self = None
    _lock = Lock()
    _bucket_name = None

    @classmethod
    def get_instance(cls):
        return MinioService()

    def __new__(cls):
        if cls._self is None:
            with cls._lock:
                if cls._self is None:
                    cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        self.client = MinioClient.get_instance().get_client()
        if self.client is None:
            raise RuntimeError("Client is not initialized")
        self._bucket_name = ApplicationConfig.get_instance().get_minio_bucket_name()

    def get_md_files(self):
        return self.client.list_objects(self._bucket_name)

    def get_md_file(self, name):
        return self.client.get_object(bucket_name=self._bucket_name, object_name=name)

    def upload_md_file(self, name, data):
        value_as_a_stream = io.BytesIO(data)
        self.client.put_object(bucket_name=self._bucket_name, object_name=name, data=value_as_a_stream, length=len(data))
