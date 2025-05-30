from asyncio import Lock

from fastapi import APIRouter

from src.server.adapter.rest.register import RegisterAPI


class MDRecordController:
    _self = None
    _lock = Lock()
    router = APIRouter(
        prefix="/api/mdrecords",
        tags=["mdrecords"],
        responses={404: {"description": "Not found"}}
    )

    @classmethod
    def get_instance(cls):
        return MDRecordController()

    def __new__(cls):
        if cls._self is None:
            with cls._lock:
                if cls._self is None:
                    cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        RegisterAPI.get_instance().register_routes(route_key="mdrecord", router=self.router)

    @router.get("/records")
    async def get_records(self):
        return

    @router.get("/records/{record_id}")
    async def get_record(self, record_id):
        return

    @router.post("/records")
    async def add_record(self):
        return
