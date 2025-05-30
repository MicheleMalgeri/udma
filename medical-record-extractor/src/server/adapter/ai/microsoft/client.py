from threading import Lock

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from src.server.config.config import ApplicationConfig


class MicrosoftClient:
    _self = None
    _lock = Lock()

    @classmethod
    def get_instance(cls):
        return MicrosoftClient()

    def __new__(cls):
        if cls._self is None:
            with cls._lock:
                if cls._self is None:
                    cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        self._config = ApplicationConfig.get_instance()

    def get_client(self):
        client = DocumentIntelligenceClient(endpoint=self._config.get_ocr_endpoint(), credential=AzureKeyCredential(self._config.get_ocr_key()))
        return client