from abc import ABC, abstractmethod


class IUserDbPort(ABC):

    @abstractmethod
    def get_users(self):
        raise NotImplementedError

    @abstractmethod
    def get_user_info_by_id(self, user_id):
        raise NotImplementedError

    @abstractmethod
    def delete_user(self, user_id):
        raise NotImplementedError

