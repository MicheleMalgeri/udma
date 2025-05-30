from abc import ABC, abstractmethod


class IOcrPort(ABC):

    @abstractmethod
    def make_ocr(self, use_microsoft=False):
        raise NotImplementedError()