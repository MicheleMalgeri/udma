from threading import Lock

from src.server.config.config import ApplicationConfig
from src.server.domain.port.db.mysql.archivedbport import IArchiveDbPort


class ArchiveRepository(IArchiveDbPort):
    _self = None
    _lock = Lock()
    _client = None
    _table_name = None

    def __new__(cls):
        if cls._self is None:
            with cls._lock:
                if cls._self is None:
                    cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        from src.server.adapter.database.mysql.client import MySqlClient
        self._client = MySqlClient.get_instance()
        self._table_name = ApplicationConfig.get_instance().get_archive()

    def get_no_ocr_records(self):
        cursor = self._client.get_connection().cursor()
        cursor.execute(f"SELECT filename FROM {self._table_name} WHERE ocr = 0")
        result = cursor.fetchall()
        return result

    def set_ocr_value(self, uda: str, ocr_value: int):
        cursor = self._client.get_connection().cursor()
        cursor.execute(f"UPDATE {self._table_name} SET ocr = {ocr_value} WHERE uda = '{uda}'")
        self._client.get_connection().commit()