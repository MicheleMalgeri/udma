from src.server.domain.model.entity.user_info import UserInfo


class UserWeight(UserInfo):
    def __init__(self, age=None, population=1, weights=None):
        super().__init__(age, population)
        self.age = age
        self.population = population
        self.normalized_population = self.normalize_population()
        self.weight = weights

    def get_weight(self):
        return self.weight

    def extend_user_info(self, user_info: UserInfo, weight):
        self.age = user_info.age
        self.population = user_info.population
        self.normalized_population = user_info.normalize_population()
        self.weight = weight
        self.cf = user_info.cf
        return self

    def to_string(self):
        print(f"Age: {self.age}, Population: {self.population} (Normalized: {self.normalized_population}), Weights: {self.weight})")

    def to_list(self):
        return [self.age, self.normalized_population, *self.weight]
