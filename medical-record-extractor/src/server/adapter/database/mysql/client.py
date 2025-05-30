from threading import Lock

import mysql.connector
from mysql.connector import errorcode

from src.server.config.config import ApplicationConfig


class MySqlClient:
    connection = None
    config = None
    _self = None
    _lock = Lock()

    @staticmethod
    def get_instance():
        return MySqlClient()

    def __new__(cls):
        if cls._self is None:
            with cls._lock:
                if cls._self is None:
                    cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        self.config = ApplicationConfig.get_instance()
        self.connection = self.connect()

    @classmethod
    def check_connection(cls, connection):
        if connection is not None:
            return True
        else:
            return False

    @classmethod
    def connect(cls):
        if cls.config is None:
            cls.config = ApplicationConfig.get_instance()
        try:
            cls.connection = mysql.connector.connect(user=cls.get_config().get_mysql_db_username(),
                                                     password=cls.get_config().get_mysql_db_password(),
                                                     host=cls.get_config().get_mysql_db_host(),
                                                     port=cls.get_config().get_mysql_db_port(),
                                                     database=cls.get_config().get_mysql_db_name())
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        return cls.get_connection()

    @classmethod
    def close_connection(cls):
        if cls.connection is not None:
            cls.connection.close()
        else:
            print("Connection already closed")

    @classmethod
    def get_connection(cls):
        return cls.connection

    @classmethod
    def get_config(cls):
        return cls.config
