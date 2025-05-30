from abc import abstractmethod, ABC


class IUserInfoDbPort(ABC):

    @abstractmethod
    def get_users_info(self):
        raise NotImplementedError

    @abstractmethod
    def get_user_info_by_id(self, user_weight_id):
        raise NotImplementedError

    @abstractmethod
    def get_last_insert_id(self):
        raise NotImplementedError

    @abstractmethod
    def delete_user_info(self, user_weight_id):
        raise NotImplementedError

    @abstractmethod
    def insert_user_info(self, user_info):
        raise NotImplementedError
