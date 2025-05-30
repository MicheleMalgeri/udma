from abc import ABC, abstractmethod

from src.server.domain.port.api.apiport import ApiPort


class AbstractFactory(ABC):

    @abstractmethod
    def create_api_port(self) -> ApiPort:
        pass

