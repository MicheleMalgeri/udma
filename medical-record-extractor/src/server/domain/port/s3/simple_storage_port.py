import abc
from abc import abstractmethod


class SimpleStoragePort(abc.ABC):

    @abstractmethod
    def get_md_files(self):
        raise NotImplementedError

    @abstractmethod
    def get_md_file(self, name):
        raise NotImplementedError

    @abstractmethod
    def upload_md_file(self, name, data):
        raise NotImplementedError