from abc import abstractmethod, ABC


class IUserWeightDbPort(ABC):

    @abstractmethod
    def get_user_weight_by_id(self, user_weight_id):
        raise NotImplementedError

    @abstractmethod
    def delete_user_weight(self, user_weight_id):
        raise NotImplementedError

    @abstractmethod
    def insert_weight(self, id: int, weight: dict):
        raise NotImplementedError

    @abstractmethod
    def insert_weight_init(self, id: int, label: str, weight: int):
        raise NotImplementedError