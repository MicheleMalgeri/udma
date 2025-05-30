from abc import ABC, abstractmethod


class IArchiveDbPort(ABC):

    @abstractmethod
    def get_no_ocr_records(self):
        raise NotImplementedError

    @abstractmethod
    def set_ocr_value(self, uda: str, ocr_value: int):
        raise NotImplementedError