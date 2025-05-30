from abc import ABC, abstractmethod

from fastapi import APIRouter


class ApiPort(ABC):

    @abstractmethod
    def register_routes(self, route_key: str, router: APIRouter):
        raise NotImplementedError

    @abstractmethod
    def get_routes(self):
        raise NotImplementedError
