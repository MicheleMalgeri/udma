from abc import ABC, abstractmethod


class ClassifierPort(ABC):

    @abstractmethod
    def evaluate_weight(self, target, users_info):
        raise NotImplementedError