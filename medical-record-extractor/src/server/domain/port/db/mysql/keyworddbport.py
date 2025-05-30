from abc import ABC, abstractmethod


class IKeywordDbPort(ABC):

    @abstractmethod
    def get_keywords(self):
        raise NotImplementedError

    @abstractmethod
    def get_keyword_by_id(self, keyword_id):
        raise NotImplementedError

    @abstractmethod
    def delete_keyword(self, keyword_id):
        raise NotImplementedError
