import os
from threading import Lock

from from_root import from_root


class ApplicationConfig:
    _self = None
    _lock = Lock()

    @staticmethod
    def get_instance():
        return ApplicationConfig()

    def __new__(cls):
        if cls._self is None:
            with cls._lock:
                if cls._self is None:
                    cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        self.__debug_mode = os.getenv('debug', 'True')
        self.__log_level = os.getenv('log_level', 'info')
        self.__mongo_db_username = os.getenv('mongo_db_username', 'root')
        self.__mongo_db_password = os.getenv('mongo_db_password', 'root')
        self.__mongo_db_client = os.getenv('mongo_db_client', 'udma')
        self.__mongo_db_name = os.getenv('mongo_db_name', 'medical_record')
        self.__mongo_db_host = os.getenv('mongo_db_host', 'localhost')
        self.__mongo_db_port = os.getenv('mongo_db_port', '27017')
        self.__mysql_db_username = os.getenv('mysql_db_username', 'admin')
        self.__mysql_db_password = os.getenv('mysql_db_password', 'root')
        self.__mysql_db_name = os.getenv('mysql_db_name', 'udma')
        self.__mysql_db_host = os.getenv('mysql_db_host', 'localhost')
        self.__mysql_db_port = os.getenv('mysql_db_port', '3307')
        self.__minio_endpoint_url = os.getenv('minio_endpoint_url', 'localhost:9000')
        self.__minio_access_key = os.getenv('minio_access_key', 'root')
        self.__minio_secret_key = os.getenv('minio_secret_key', 'password')
        self.__minio_bucket_name = os.getenv('minio_bucket_name', 'mdfiles')
        self.__model_name = os.getenv('model_name', 'llama-3-8b-gpt-4o-ru1.0@q2_k')
        self.__ocr_endpoint = os.getenv('ocr_endpoint', '')
        self.__ocr_key = os.getenv('ocr_key', '')
        self.__ocr_call_per_minute = os.getenv('ocr_call_per_minute', 10)
        self.__record_ocr_path = os.getenv('record_ocr_path', from_root('resources/medical_records_ocr'))
        self.__knn_threshold = os.getenv('knn_threshold', 2)
        self.__keywords = os.getenv('keywords', 'udma.keywords')
        self.__labels = os.getenv('keywords', 'udma.labels')
        self.__user_info = os.getenv('keywords', 'udma.user_info')
        self.__user_weights = os.getenv('keywords', 'udma.user_weights')
        self.__archive = os.getenv('keywords', 'udma.mr_archive')
        self.__census = os.getenv('keywords', 'udma.census')
        self.__n_threshold = os.getenv('n_threshold', 1)
        self.__batch_time = os.getenv('batch_time', "00:30")
        self.__unknown_response = os.getenv('unknown_response', "No, non ricordo")
        self.__inactivity_timeout = os.getenv('inactivity_timeout', 120)


    def get_debug_mode(self):
        return self.__debug_mode

    def get_log_level(self):
        return self.__log_level

    def get_mongo_db_username(self):
        return self.__mongo_db_username

    def get_mongo_db_password(self):
        return self.__mongo_db_password

    def get_mongo_db_client(self):
        return self.__mongo_db_client

    def get_mongo_db_name(self):
        return self.__mongo_db_name

    def get_mongo_db_host(self):
        return self.__mongo_db_host

    def get_mongo_db_port(self):
        return self.__mongo_db_port

    def get_mysql_db_name(self):
        return self.__mysql_db_name

    def get_mysql_db_host(self):
        return self.__mysql_db_host

    def get_mysql_db_port(self):
        return self.__mysql_db_port

    def get_mysql_db_username(self):
        return self.__mysql_db_username

    def get_mysql_db_password(self):
        return self.__mysql_db_password

    def get_minio_endpoint_url(self):
        return self.__minio_endpoint_url

    def get_minio_access_key(self):
        return self.__minio_access_key

    def get_minio_secret_key(self):
        return self.__minio_secret_key

    def get_minio_bucket_name(self):
        return self.__minio_bucket_name

    def get_model_name(self):
        return self.__model_name

    def get_ocr_endpoint(self):
        return self.__ocr_endpoint

    def get_ocr_key(self):
        return self.__ocr_key

    def get_ocr_call_per_minute(self):
        return self.__ocr_call_per_minute

    def get_record_ocr_path(self):
        return self.__record_ocr_path

    def get_knn_threshold(self):
        return self.__knn_threshold

    def get_keywords(self):
        return self.__keywords

    def get_labels(self):
        return self.__labels

    def get_user_info(self):
        return self.__user_info

    def get_user_weights(self):
        return self.__user_weights

    def get_census(self):
        return self.__census

    def get_archive(self):
        return self.__archive

    def get_n_threshold(self):
        return self.__n_threshold

    def get_batch_time(self):
        return self.__batch_time

    def get_unknown_response(self):
        return self.__unknown_response

    def get_inactivity_timeout(self):
        return self.__inactivity_timeout

