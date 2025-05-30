from threading import Lock

from src.server.adapter.database.mysql.client import MySqlClient
from src.server.domain.model.entity.user_info import UserInfo
from src.server.domain.port.db.mysql.userdbport import IUserDbPort


class UserRepository(IUserDbPort):
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
        self._client = MySqlClient.get_instance()
        self._table_name = ""

    def get_users(self):
        cursor = self._client.get_connection().cursor()
        cursor.execute(f"SELECT * FROM {self._table_name}")
        results = cursor.fetchall()
        return self.__list_to_user_dto(results)

    def get_user_info_by_id(self, user_id):
        cursor = self._client.get_connection().cursor()
        cursor.execute(f"SELECT * FROM {self._table_name} WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        if result is None:
            return None
        return UserInfo().from_list(result)

    def delete_user(self, user_id):
        cursor = self._client.get_connection().cursor()
        cursor.execute(f"DELETE FROM {self._table_name} WHERE id = %s", (user_id,))
        self._client.get_connection().commit()
        cursor.close()

    @staticmethod
    def __list_to_user_dto(results):
        user_info_dto = list()
        for result in results:
            user_info_dto.append(UserInfo().from_list(result))
        return user_info_dto
