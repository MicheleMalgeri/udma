from threading import Lock

from src.server.domain.model.label import Labels
from src.server.domain.port.decision.decisionport import DecisionPort


class GiniImpurity(DecisionPort):
    _self = None
    _lock = Lock()
    _keywords = None
    _label_weights = None

    @classmethod
    def get_instance(cls):
        return GiniImpurity()

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            with cls._lock:
                if cls._self is None:
                    cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        self._df = None
        self._label_weights = None
        self._keywords = None

    def __prob_of_diagnosis(self):
        keywords = self.__get_used_keywords()
        p_sum = 0
        for record in self._df[Labels.KEYWORDS.name]:
            p_sum += (len(record) / len(keywords)) ** 2
        return p_sum

    def __get_used_keywords(self):
        keywords = list()
        for record in self._df[Labels.KEYWORDS.name]:
            keywords.extend(record)
        return set(keywords)

    def __prob_of_attribute(self, class_name, attribute):
        n = len(self._df[class_name])
        n_k = len(self._df[self._df[class_name] == attribute])
        return n_k / n

    def __gini_attribute(self):
        gini_values = list()
        for column in self._df.columns:
            if column not in self._label_weights:
                continue
            p_sum = 0
            attributes = self._df[column].unique()
            if column == Labels.DIAGNOSI.name:
                p_sum = self.__prob_of_diagnosis()
            else:
                for attribute in attributes:
                    p_sum += self.__prob_of_attribute( column, attribute) ** 2
            value = (1 - p_sum) * self._label_weights[column]
            gini_values.append([column, value])
        return gini_values

    def get_decision_feature(self, df, label_weights, keywords):
        self._df = df
        self._label_weights = label_weights
        self._keywords = keywords
        gini_values = self.__gini_attribute()
        return max(gini_values, key=lambda x: x[1])[0]
