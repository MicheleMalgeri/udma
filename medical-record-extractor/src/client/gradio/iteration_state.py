from threading import Lock

from pkg.lib.utils import json_to_dataframe
from src.server.domain.model.chat_prompt import ChatPrompt
from src.server.config.config import ApplicationConfig
from src.server.domain.model.entity.user_info import UserInfo
from src.server.domain.model.entity.user_weight import UserWeight
from src.server.domain.port.db.mongo.mddbport import IMdDbPort
from src.server.domain.port.db.mysql.keyworddbport import IKeywordDbPort
from src.server.domain.port.db.mysql.labeldbport import ILabelDbPort
from src.server.domain.port.db.mysql.userinfodbport import IUserInfoDbPort
from src.server.domain.port.db.mysql.userweightdbport import IUserWeightDbPort
from src.server.domain.port.decision.decisionport import DecisionPort
from src.server.domain.port.nlp.inlpport import INlpPort
from src.server.domain.port.s3.simple_storage_port import SimpleStoragePort


class IterationState:
    _self = None
    _lock = Lock()
    _iteration = None
    _labels = None
    _weights = None  # pesi che andranno a db (se sa rispondere è 1)
    _weights_local = None  # pesi per l'interazione corrente (dopo una domanda, va a 0)
    _questions = None
    _medical_records = None
    _n_threshold = None
    _user_info = None

    @classmethod
    def get_instance(cls, user: UserWeight):
        return IterationState(user=user)

    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            with cls._lock:
                if cls._self is None:
                    cls._self = super().__new__(cls)
        return cls._self

    def __init__(self, user: UserWeight):
        self._iteration = 0
        self._labels = ILabelDbPort().get_active_labels()
        self._questions = self.__labels_dto_to_dict()
        self._medical_records = IMdDbPort().get_medical_record_by_cf(user.get_cf())
        self._weights = user.get_weight().copy()
        self._weights_local = user.get_weight().copy()
        self._n_threshold = ApplicationConfig().get_n_threshold()
        self.pending_question = None
        self.pending_gini_feat = None
        self._user_info = UserInfo(age=user.get_age(), population=user.get_population())

    def get_iteration(self):
        return self._iteration

    def get_labels(self):
        return self._labels

    def get_weights(self):
        return self._weights

    def get_weights_local(self):
        return self._weights_local

    def get_questions(self):
        return self._questions

    def get_medical_records(self):
        return self._medical_records

    def get_pending_question(self):
        return self.pending_question

    def get_pending_gini_feat(self):
        return self.pending_gini_feat

    def __labels_dto_to_dict(self):
        result = dict()
        for label_dto in self._labels:
            result[label_dto.get_name()] = label_dto.get_user_question()
        return result

    def __evaluate_gini_feat(self):
        df = json_to_dataframe(self._medical_records)
        decision_feature = DecisionPort().get_decision_feature(df, self._weights, IKeywordDbPort().get_keywords())
        if decision_feature == "Keywords":
            return "Diagnosi"
        return decision_feature

    def __evaluate_question(self, label: str) -> str:
        question = self._questions[label]
        return question

    @staticmethod
    def __evaluate_user_answer(answer: str) -> int:
        if answer == "No, non ricordo":
            return 0
        else:
            return 1

    def __update_weights(self, label: str, global_value: int):
        self._weights[label] = global_value
        self._weights_local[label] = 0

    def __filter_records(self, answer, label):
        medical_record_filtered = list()
        for record in self._medical_records:
            text = f"Questa risposta: \"{answer}\", si potrebbe riferire a: \"{record[label]}\"?"
            print(text)
            bot_answer = INlpPort().interaction(ChatPrompt.YN_PROMPT, text)
            if bot_answer.lower().strip(".") != "no":
                medical_record_filtered.append(record)
        self._medical_records = medical_record_filtered

    def evaluate_medical_records_length(self):
        n = len(self._medical_records)
        if n == 0:
            self.__save_user()
            return "Termine: nessun record trovato.", []
        texts, files = self.__summarize_records()
        if n == 1:
            message = f"Termine: cartella clinica trovata!\n{texts[0]}"
            self.__save_user()
            return message, files
        if n < self._n_threshold:
            joined = "\n\n".join(texts)
            message = f"Termine: {n} cartelle cliniche trovate!\n{joined}"
            self.__save_user()
            return message, files
        return None

    def generate_question(self, knows_answer=1):
        self._iteration += 1
        if self._iteration == 1:
            prefix = "Per iniziare, "
        elif knows_answer == 0:
            prefix = "Ok, proviamo con un'altra domanda. Se ricordi, "
        elif len(self._medical_records) > 2 * self._n_threshold:
            prefix = f"Ho ristretto il campo a {len(self._medical_records)} record. Per migliorare la ricerca, "
        else:
            prefix = "Ci siamo quasi! Per identificare il record corretto, "
        gini_feat = self.__evaluate_gini_feat()
        question = self.__evaluate_question(gini_feat)
        self.pending_question = question
        self.pending_gini_feat = gini_feat
        return prefix + question

    def process_answer(self, user_answer):
        knows_answer = self.__evaluate_user_answer(user_answer)
        self.__update_weights(self.pending_gini_feat, knows_answer)
        if knows_answer == 1:
            self.__filter_records(user_answer, self.pending_gini_feat)
            print("Sono rimasti: ", len(self._medical_records), " record.")
            termination_message = self.evaluate_medical_records_length()
            if termination_message is not None:
                return termination_message
        if all(value == 0 for value in self._weights_local.values()):
            print("Domande da porre terminate!")
            return "Termine: nessun record trovato."
        return self.generate_question(knows_answer)

    @staticmethod
    def check_lms_connection():
        return INlpPort().check_connection()

    @staticmethod
    def __format_record(rec):
        text = (
            f"  • UDA: {rec['UDA']}\n"
            f"  • Ricovero n. {rec['Numero Ricovero']} del {rec['Data Ricovero']}\n"
            f"  • Reparto Accettazione: {rec['Reparto Accettazione']}\n"
            f"  • Diagnosi: {rec['Diagnosi']}\n"
        )
        uri = rec['URI']
        minio_response = SimpleStoragePort().get_md_file(uri)
        file_data = (uri, minio_response)
        return text, file_data

    def __summarize_records(self):
        texts = []
        files = []
        for rec in self._medical_records:
            t, f = self.__format_record(rec)
            texts.append(t)
            if f:
                files.append(f)
        return texts, files

    def __save_user(self):
        user_id = IUserInfoDbPort().insert_user_info(self._user_info)
        IUserWeightDbPort().insert_weight(user_id, self._weights)
