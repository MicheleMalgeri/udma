from threading import Lock

from src.server.adapter.database.mongo.client import MongoDBClient
from src.server.config.config import ApplicationConfig
from src.server.domain.port.db.mongo.mddbport import IMdDbPort


class MedicalRepository(IMdDbPort):
    _self = None
    _lock = Lock()
    _collection = None

    def __new__(cls):
        if cls._self is None:
            with cls._lock:
                if cls._self is None:
                    cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        self._client = MongoDBClient.get_instance()
        db = self._client.get_client()[ApplicationConfig.get_instance().get_mongo_db_client()]
        self._collection = db[ApplicationConfig.get_instance().get_mongo_db_name()]


    def get_medical_record_by_cf(self, codice_fiscale: str):
        return list(self._collection.find({"Codice Fiscale": codice_fiscale}))

    def get_medical_records_by_user(self, fiscal_code: str):
        return

    def save_medical_record(self, record):
        return

    def insert_medical_record(self, record):
        self._collection.insert_one(record)

    def get_all_medical_records(self):
        return list(self._collection.find())

    def deactivate_medical_record(self, medical_id: str):
        return
