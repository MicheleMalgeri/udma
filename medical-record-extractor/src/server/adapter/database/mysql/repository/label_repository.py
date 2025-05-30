from threading import Lock

from src.server.config.config import ApplicationConfig
from src.server.domain.model.entity.label import LabelDTO
from src.server.domain.port.db.mysql.labeldbport import ILabelDbPort


class LabelRepository(ILabelDbPort):
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
        self._table_name = ApplicationConfig.get_instance().get_labels()

    def get_all_labels(self):
        cursor = self._client.get_connection().cursor()
        cursor.execute(f"SELECT * FROM {self._table_name}")
        results = cursor.fetchall()
        return self.__list_to_dto(results)

    def get_active_labels(self):
        cursor = self._client.get_connection().cursor()
        cursor.execute(f"SELECT * FROM {self._table_name} WHERE is_active = 1")
        results = cursor.fetchall()
        return self.__list_to_dto(results)

    def get_primary_labels(self):
        cursor = self._client.get_connection().cursor()
        cursor.execute(f"SELECT * FROM {self._table_name} WHERE is_primary = 1")
        results = cursor.fetchall()
        return self.__list_to_dto(results)

    def get_label_by_late_value(self, late_value: int):
        cursor = self._client.get_connection().cursor()
        cursor.execute(f"SELECT * FROM {self._table_name} WHERE is_late = {late_value}")
        results = cursor.fetchall()
        return self.__list_to_dto(results)

    def get_all_labels_for_ocr(self):
        cursor = self._client.get_connection().cursor()
        cursor.execute(f"SELECT * FROM {self._table_name} WHERE is_late = 0 AND is_anag = 0")
        results = cursor.fetchall()
        return self.__list_to_dto(results)

    def get_label_by_name(self, label_name):
        cursor = self._client.get_connection().cursor()
        cursor.execute(f"SELECT * FROM {self._table_name} WHERE label_name = '{label_name}'")
        result = cursor.fetchone()
        return LabelDTO().from_list(result)

    def delete_label(self, label_id):
        cursor = self._client.get_connection().cursor()
        cursor.execute(f"DELETE FROM {self._table_name} WHERE label_name = {label_id}")
        self._client.get_connection().commit()

    @staticmethod
    def __list_to_dto(results) -> list:
        labels_dto = list()
        for result in results:
            labels_dto.append(LabelDTO().from_list(result))
        return labels_dto
