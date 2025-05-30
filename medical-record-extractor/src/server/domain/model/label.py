from enum import Enum


class Label:
    def __init__(self, name):
        self.name = name
        self.db_name = name.lower().replace(" ", "_")


class Labels(Enum):
    URI = Label("Uri")
    UDA = Label("UDA")
    ANNO_RICOVERO = Label("Anno Ricovero")
    NUMERO_RICOVERO = Label("Numero Ricovero")
    REGIME = Label("Regime")
    COGNOME = Label("Cognome")
    NOME = Label("Nome")
    SESSO = Label("Sesso")
    DATA_NASCITA = Label("Data Nascita")
    COMUNE_NASCITA = Label("Comune Nascita")
    COMUNE_RESIDENZA = Label("Comune Residenza")
    CODICE_FISCALE = Label("Codice Fiscale")
    DATA_RICOVERO = Label("Data Ricovero")
    REPARTO_ACCETTAZIONE = Label("Reparto Accettazione")
    TIPO_RICOVERO = Label("Tipo Ricovero")
    REPARTO_DIMISSIONE = Label("Reparto Dimissione")
    DATA_DIMISSIONE = Label("Data Dimissione")
    ANAMNESI = Label("Anamnesi")
    DIAGNOSI = Label("Diagnosi")
    TERAPIA = Label("Terapia")
    KEYWORDS = Label("Keywords")
    OCR = Label("Ocr")
