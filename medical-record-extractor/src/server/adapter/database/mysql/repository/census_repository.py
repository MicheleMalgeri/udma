from threading import Lock

from src.server.config.config import ApplicationConfig
from src.server.domain.port.db.mysql.censusdbport import ICensusDbPort


class CensusRepository(ICensusDbPort):
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
        self._table_name = ApplicationConfig.get_instance().get_census()

    def get_population_by_city(self, name: str) -> int:
        cursor = self._client.get_connection().cursor()
        cursor.execute(f"SELECT population FROM {self._table_name} WHERE city = '{name}'")
        result = cursor.fetchone()
        if result:
            return result[0]
        return 0
