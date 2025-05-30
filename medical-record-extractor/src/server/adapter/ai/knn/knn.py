import math
from itertools import islice
from threading import Lock

from src.server.config.config import ApplicationConfig
from src.server.domain.model.entity.user_info import UserInfo
from src.server.domain.port.classifier.classifierport import ClassifierPort
from src.server.domain.port.db.mysql.userweightdbport import IUserWeightDbPort


class KNN(ClassifierPort):
    _self = None
    _lock = Lock()
    _k = None
    _target = None
    _users_info = []
    _k_distances = None

    @classmethod
    def get_instance(cls):
        return KNN()

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            with cls._lock:
                if cls._self is None:
                    cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        self._k = ApplicationConfig().get_knn_threshold()
        self._target = None
        self._users_info = []

    @staticmethod
    def __user_euclidean_distance(user1: UserInfo, user2: UserInfo) -> float:
        return math.sqrt(
            (user1.age - user2.age) ** 2 + (user1.normalized_population - user2.normalized_population) ** 2)

    def __get_user_distances(self) -> dict:
        distances = dict()
        for user in self._users_info:
            dist = self.__user_euclidean_distance(user, self._target)
            distances[user] = dist
        return distances

    def __get_k_distances(self) -> None:
        distances = self.__get_user_distances()
        sorted_dict = dict(sorted(distances.items(), key=lambda item: item[1]))
        self._k_distances = self.__take_first_k(sorted_dict.items())

    def __take_first_k(self, iterable) -> list:
        return list(islice(iterable, self._k))

    def __get_weights(self) -> list:
        weights = []
        for item in self._k_distances:
            user_info = item[0]
            distance = item[1]
            if distance == 0:
                distance = 1e-10  # Avoid division by zero
            weight_list = IUserWeightDbPort().get_user_weight_by_id(user_info.id)
            weights.extend(self.__extract_weights(weight_list, distance))
        return weights

    @staticmethod
    def __extract_weights(weights: list, distance: float) -> list:
        extracted_weights = []
        for weight in weights:
            label = weight[1]
            weight_value = weight[2] / distance
            dict_temp = dict()
            dict_temp[label] = weight_value
            extracted_weights.append(dict_temp)
        return extracted_weights

    def __merge_weights(self, weights: list) -> dict:
        summed_values = {}
        for weight in weights:
            for k, v in weight.items():
                summed_values[k] = summed_values.get(k, 0) + v
        return {key: summed_values[key] / self._k for key in summed_values}

    def evaluate_weight(self, target: UserInfo, users_info: list) -> dict:
        self._target = target
        self._users_info = users_info
        self.__get_k_distances()
        weights = self.__get_weights()
        return self.__merge_weights(weights)
