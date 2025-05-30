from threading import Lock

from src.server.adapter.rest.register import RegisterAPI
from src.server.domain.port.api.apiport import ApiPort
from src.server.domain.factory.abstract_factory import AbstractFactory


class ConcreteFactory(AbstractFactory):
    _self = None
    _lock = Lock()

    @classmethod
    def get_instance(cls):
        return ConcreteFactory()

    def __new__(cls):
        if cls._self is None:
            with cls._lock:
                if cls._self is None:
                    cls._self = super().__new__(cls)
        return cls._self

    def create_api_port(self) -> ApiPort:
        return RegisterAPI()
