from threading import Lock

from src.server.config.config import ApplicationConfig
from src.server.domain.model.entity.user_info import UserInfo
from src.server.domain.port.db.mysql.userinfodbport import IUserInfoDbPort


class UserInfoRepository(IUserInfoDbPort):
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
        self._table_name = ApplicationConfig.get_instance().get_user_info()

    def get_users_info(self):
        cursor = self._client.get_connection().cursor()
        cursor.execute(f"SELECT * FROM {self._table_name}")
        results = cursor.fetchall()
        return self.__list_to_user_dto(results)

    def get_user_info_by_id(self, user_info_id):
        cursor = self._client.get_connection().cursor()
        cursor.execute(f"SELECT * FROM {self._table_name} WHERE id = {user_info_id}")
        result = cursor.fetchone()
        return result

    def get_last_insert_id(self):
        cursor = self._client.get_connection().cursor()
        cursor.execute("SELECT LAST_INSERT_ID()")
        result = cursor.fetchone()
        return result[0]

    def insert_user_info(self, user_info: UserInfo):
        cursor = self._client.get_connection().cursor()
        cursor.execute(
            f"INSERT INTO {self._table_name} (age, population) VALUES ({user_info.get_age()}, {user_info.get_population()})")
        self._client.get_connection().commit()
        return self.get_last_insert_id()

    def delete_user_info(self, user_info_id):
        cursor = self._client.get_connection().cursor()
        cursor.execute(f"DELETE FROM {self._table_name} WHERE id = {user_info_id}")
        self._client.get_connection().commit()

    @staticmethod
    def __list_to_user_dto(results):
        user_info_dto = list()
        for result in results:
            user_info_dto.append(UserInfo().from_list(result))
        return user_info_dto