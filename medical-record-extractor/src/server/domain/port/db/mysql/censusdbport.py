from abc import ABC, abstractmethod


class ICensusDbPort(ABC):

    @abstractmethod
    def get_population_by_city(self, name: str) -> int:
        raise NotImplementedError
