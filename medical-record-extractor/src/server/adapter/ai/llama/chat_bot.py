import lmstudio as lms

from src.server.config.config import ApplicationConfig
from src.server.domain.port.nlp.inlpport import INlpPort


class ChatBot(INlpPort):
    def __init__(self):
        self.model = lms.llm(ApplicationConfig().get_model_name())
        self.chat = None

    def interaction(self, chat_prompt, message, print_stream=True):
        self.chat = lms.Chat(chat_prompt.value)
        self.chat.add_user_message(message)
        if print_stream:
            prediction_stream = self.model.respond_stream(
                self.chat,
                on_message=self.chat.append,
            )
            return self.__stream_and_respond(prediction_stream)
        else:
            return self.model.respond(message)

    @staticmethod
    def __stream_and_respond(prediction_stream):
        answer = str()
        print("Bot: ", end="", flush=True)
        for fragment in prediction_stream:
            answer += fragment.content
            print(fragment.content, end="", flush=True)
        print()
        return answer

    def check_connection(self):
        try:
            lms.llm(ApplicationConfig().get_model_name())
            return True
        except Exception as e:
            print(f"Error connecting to LLM: {e}")
            return False