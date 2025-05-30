from threading import Lock

from src.server.adapter.database.mysql.repository.label_repository import LabelRepository
from src.server.config.config import ApplicationConfig
from src.server.domain.port.db.mysql.userweightdbport import IUserWeightDbPort


class UserWeightRepository(IUserWeightDbPort):
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
        self._table_name = ApplicationConfig.get_instance().get_user_weights()

    def get_user_weight_by_id(self, user_weight_id):
        cursor = self._client.get_connection().cursor()
        cursor.execute(f"SELECT * FROM {self._table_name} WHERE uid = {user_weight_id}")
        result = cursor.fetchall()
        return result

    def delete_user_weight(self, user_weight_id):
        cursor = self._client.get_connection().cursor()
        cursor.execute(f"DELETE FROM {self._table_name} WHERE uid = {user_weight_id}")
        self._client.get_connection().commit()

    def insert_weight(self, id: int, weight: dict):
        labels = LabelRepository().get_active_labels()
        for label in labels:
            label_name = label.get_name()
            cursor = self._client.get_connection().cursor()
            cursor.execute(f"INSERT INTO {self._table_name} (uid, label, value) VALUES ('{id}', '{label_name}', '{weight[label_name]}')")
            self._client.get_connection().commit()

    def insert_weight_init(self, id: int, label: str, weight: int):
        cursor = self._client.get_connection().cursor()
        cursor.execute(f"INSERT INTO {self._table_name} (uid, label, value) VALUES ('{id}', '{label}', '{weight}')")
        self._client.get_connection().commit()