from abc import ABC, abstractmethod


class DecisionPort(ABC):

    @abstractmethod
    def get_decision_feature(self, df, label_weights, keywords):
        raise NotImplementedError()