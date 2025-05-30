import math


class UserInfo:
    def __init__(self, id=None, age=None, population=1, cf=None):
        self.id = id
        self.age = age
        self.population = population
        self.normalized_population = self.normalize_population()
        self.cf = cf

    def get_age(self):
        return int(self.age)

    def get_population(self):
        return int(self.population)

    def normalize_population(self):
        return (math.log(self.population, 10)) * 10

    def get_cf(self):
        return self.cf

    def to_string(self):
        print(f"Age: {self.age}, Population: {self.population} (Normalized: {self.normalized_population})")

    def from_list(self, data):
        self.id = data[0]
        self.age = data[1]
        self.population = data[2]
        self.normalized_population = self.normalize_population()
        return self

    def to_list(self):
        return [self.age, self.normalized_population]

    def user_info(self):
        return [self.age, self.population]
