from abc import ABC, abstractmethod


class INlpPort(ABC):

    @abstractmethod
    def interaction(self, chat_prompt, message, print_stream=True):
        raise NotImplementedError()

    @abstractmethod
    def check_connection(self):
        raise NotImplementedError()