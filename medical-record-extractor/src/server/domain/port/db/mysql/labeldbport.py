from abc import ABC, abstractmethod


class ILabelDbPort(ABC):

    @abstractmethod
    def get_all_labels(self):
        raise NotImplementedError

    @abstractmethod
    def get_label_by_name(self, label_name):
        raise NotImplementedError

    @abstractmethod
    def delete_label(self, label_id):
        raise NotImplementedError

    @abstractmethod
    def get_active_labels(self):
        raise NotImplementedError

    @abstractmethod
    def get_primary_labels(self):
        raise NotImplementedError

    @abstractmethod
    def get_label_by_late_value(self, late_value: int):
        raise NotImplementedError

    @abstractmethod
    def get_all_labels_for_ocr(self):
        raise NotImplementedError
