from threading import Lock

from src.server.adapter.database.mysql.client import MySqlClient
from src.server.config.config import ApplicationConfig
from src.server.domain.port.db.mysql.keyworddbport import IKeywordDbPort


class KeywordRepository(IKeywordDbPort):
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
        self._table_name = ApplicationConfig.get_instance().get_keywords()

    def get_keywords(self):
        cursor = self._client.get_connection().cursor()
        cursor.execute(f"SELECT * FROM {self._table_name}")
        result = cursor.fetchall()
        return self.extract_keyword(result)

    @staticmethod
    def extract_keyword(keywords):
        result = []
        for keyword in keywords:
            result.append(keyword[0])
        return result

    def get_keyword_by_id(self, keyword_id):
        return

    def delete_keyword(self, keyword_id):
        return
