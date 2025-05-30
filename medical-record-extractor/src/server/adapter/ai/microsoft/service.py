import base64
import os
from datetime import timedelta
from io import BytesIO
from threading import Lock

from PyPDF2 import PdfReader, PdfWriter

from pkg.lib.utils import open_txt_file, get_time, wait_time_for_sleep
from src.server.adapter.ai.microsoft.client import MicrosoftClient
from src.server.domain.model.chat_prompt import ChatPrompt
from src.server.config.config import ApplicationConfig
from src.server.domain.model.entity.label import LabelDTO
from src.server.domain.model.label import Labels
from src.server.domain.port.db.mongo.mddbport import IMdDbPort
from src.server.domain.port.db.mysql.archivedbport import IArchiveDbPort
from src.server.domain.port.db.mysql.labeldbport import ILabelDbPort
from src.server.domain.port.nlp.inlpport import INlpPort
from src.server.domain.port.ocr.iocrport import IOcrPort
from src.server.domain.port.s3.simple_storage_port import SimpleStoragePort


class MicrosoftService(IOcrPort):
    _self = None
    _lock = Lock()

    @classmethod
    def get_instance(cls):
        return MicrosoftService()

    def __new__(cls):
        if cls._self is None:
            with cls._lock:
                if cls._self is None:
                    cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        self.client = MicrosoftClient().get_instance().get_client()
        if self.client is None:
            raise RuntimeError("Client is not initialized")

    def make_ocr(self, use_microsoft=False):
        medical_records = self._get_records()
        if use_microsoft:
            client = MicrosoftClient.get_instance().get_client()
            end_time = get_time() - timedelta(seconds=10)
            for medical_record in medical_records:
                current_time = get_time()
                wait_time_for_sleep(current_time, end_time)
                raw_text = self._make_ocr(medical_record, client)
                end_time = get_time()
                medical_record_ocr = self._build_medical_record_object(raw_text)
                IMdDbPort().insert_medical_record(medical_record_ocr)
                IArchiveDbPort().set_ocr_value(medical_record_ocr[Labels.UDA], 1)
        else:
            medical_record_path = ApplicationConfig.get_instance().get_record_ocr_path()
            for filename in os.listdir(medical_record_path):
                raw_text = open_txt_file(os.path.join(medical_record_path, filename))
                d = self.__data_extractor(raw_text)
                IMdDbPort().insert_medical_record(d)

    def _build_medical_record_object(self, raw_text):
        medical_record = self.__data_extractor(raw_text)
        medical_record[Labels.OCR] = 1
        medical_record["_id"] = f"{medical_record[Labels.CODICE_FISCALE]}_{medical_record[Labels.UDA]}"
        return medical_record

    @classmethod
    def _get_records(cls):
        results = list()
        medical_records = IArchiveDbPort().get_no_ocr_records()
        for record in medical_records:
            filename = record[0]
            response = SimpleStoragePort().get_md_file(filename)
            response_data = bytes()
            for d in response.stream():
                response_data += d
            pdf_data = BytesIO(response_data)
            output_pdf = cls._get_first_page(pdf_data)
            first_page_base64 = base64.b64encode(output_pdf.getvalue()).decode("utf-8")
            results.append(first_page_base64)
        return results

    @staticmethod
    def _make_ocr(base64_encoded_pdf, client):
        text = str()
        analyze_request = {"base64Source": base64_encoded_pdf}
        poller = client.begin_analyze_document("prebuilt-read", analyze_request)
        result = poller.result()
        text += " ".join(line.content for page in result.pages if page.lines for line in page.lines)
        return text

    @staticmethod
    def _get_first_page(pdf_data):
        input_pdf = PdfReader(pdf_data)
        writer = PdfWriter()
        writer.add_page(input_pdf.pages[0])
        output_pdf = BytesIO()
        writer.write(output_pdf)
        return output_pdf

    @classmethod
    def __feature_extractor_bot(cls, text, question) -> str:
        return rf"Considera questo testo: {text}. {question}"

    @classmethod
    def __feature_extractor(cls, text) -> str:
        return INlpPort().interaction(ChatPrompt.GENERIC_PROMPT, text)

    @classmethod
    def __keyword_extractor(cls, text) -> str:
        return INlpPort().interaction(ChatPrompt.KEYWORDS_PROMPT, text)

    @classmethod
    def __data_extractor(cls, doc) -> dict:
        label_schema = dict()
        labels_dto = [LabelDTO().from_list(label) for label in ILabelDbPort().get_all_labels_for_ocr()]
        for label in labels_dto:
            label_name = label.get_name()
            label_question = label.get_question()
            text_input = cls.__feature_extractor_bot(doc, label_question)
            bot_answer = cls.__feature_extractor(text_input)
            label_schema[label_name] = bot_answer
            if label_name == Labels.DIAGNOSI.name:
                label_schema[Labels.KEYWORDS.name] = cls.__keyword_extractor(bot_answer)
        return label_schema
