class LabelDTO:
    def __init__(self, name=None, is_active=None, is_primary=None, is_late=None, is_anag=None, question=None, user_question=None):
        self._name = name
        self._is_active = is_active
        self._is_primary = is_primary
        self._is_late = is_late
        self._is_anag = is_anag
        self._question = question
        self._user_question = user_question

    def get_name(self):
        return self._name

    def get_is_active(self):
        return self._is_active

    def get_is_primary(self):
        return self._is_primary

    def get_is_late(self):
        return self._is_late

    def get_is_anag(self):
        return self._is_anag

    def get_question(self):
        return self._question

    def get_user_question(self):
        return self._user_question

    def from_list(self, data):
        self._name = data[0]
        self._is_active = data[1] == 1
        self._is_primary = data[2] == 1
        self._is_late = data[3] == 1
        self._is_anag = data[4] == 1
        self._question = data[5]
        self._user_question = data[6]
        return self

    def to_string(self):
        print(
            f"Label: {self._name}, Active: {self._is_active}, Primary: {self._is_primary}, Late: {self._is_late}, Anag: {self._is_anag}, Question: {self._question}, User Question: {self._user_question}")
