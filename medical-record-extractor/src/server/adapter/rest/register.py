from threading import Lock

from fastapi import APIRouter

from src.server.domain.port.api.apiport import ApiPort


class RegisterAPI(ApiPort):
    _self = None
    _lock = Lock()
    _routes = {}

    @classmethod
    def get_instance(cls):
        return RegisterAPI()

    def __new__(cls):
        if cls._self is None:
            with cls._lock:
                if cls._self is None:
                    cls._self = super().__new__(cls)
        return cls._self

    def register_routes(self, route_key: str, route: APIRouter):
        self._routes[route_key] = route

    def get_routes(self):
        return self._routes
