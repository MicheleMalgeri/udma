class MedicalKeywords:
    def __init__(self):
        self.keywords = [
            "Alzheimer",
            "Schizofrenia",
            "Bipolare",
            "Scompenso",
            "Glicemia",
            "Emorragia",
            "Infezione",
            "Infarto",
            "Ipertensione",
            "Diabete",
            "Tumore",
            "Neoplasia",
            "Polmonite",
            "Asma",
            "Artrite",
            "Bronchite",
            "Epatite",
            "Insufficienza cardiaca",
            "Insufficienza renale",
            "Insufficienza epatica",
            "Insufficienza respiratoria",
            "Insufficienza venosa",
            "Insufficienza arteriosa",
            "Insufficienza circolatoria",
            "Insufficienza linfatica",
            "Complicanze",
            "Lesione",
            "Infiammazione",
            "Sepsi",
            "Ulcera",
            "Edema polmonare",
            "Edema cerebrale",
            "Edema periferico",
            "Edema linfatico",
            "Edema venoso",
            "Edema arterioso",
            "Edema circolatorio",
            "Edema cardiaco",
            "Ictus",
            "Ischemia",
            "Anemia",
            "Cefalea",
            "Cistite",
            "Dermatite",
            "Mialgia",
            "Neuropatia",
            "Diarrea",
            "Psoriasi",
            "Ernia",
            "Distaccamento retina",
            "Distorsione",
            "Frattura",
            "Lussazione",
            "Ematoma",
            "Emorragia",
            "Trombosi",
            "Embolia",
            "Tachicardia",
            "Bradicardia",
            "Aritmia",
            "Fibrillazione",
            "Tachipnea",
            "Dispnea",
            "Epilessia",
        ]

    def get_keywords_as_string(self):
        return str(self.keywords).replace("'", "").replace("[", "").replace("]", "")
