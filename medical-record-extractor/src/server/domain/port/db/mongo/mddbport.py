from abc import ABC, abstractmethod


class IMdDbPort(ABC):

    @abstractmethod
    def get_medical_record_by_cf(self, codice_fiscale: str):
        raise NotImplementedError()

    @abstractmethod
    def get_medical_records_by_user(self, fiscal_code: str):
        raise NotImplementedError()

    @abstractmethod
    def save_medical_record(self, record):
        raise NotImplementedError()

    @abstractmethod
    def insert_medical_record(self, record):
        raise NotImplementedError()

    @abstractmethod
    def deactivate_medical_record(self, medical_id: str):
        raise NotImplementedError()