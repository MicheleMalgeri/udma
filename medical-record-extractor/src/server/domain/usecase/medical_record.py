from src.server.domain.port.db.mongo.mddbport import IMdDbPort
from src.server.domain.port.db.mysql.userdbport import IUserDbPort


class MedicalRecordService:
    _md_repository: IMdDbPort
    _user_repository: IUserDbPort

    def __init__(self, md_repository_impl, user_repository_impl):
        self._md_repository = md_repository_impl
        self._user_repository = user_repository_impl

    def show_medical_record(self, medical_id: str):
        return self._md_repository.get_medical_record_by_id(medical_id)

    def show_users(self):
        return self._user_repository.get_users()
