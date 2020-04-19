# wykys 2020
# knihovna pro práci s korpusem


class Record(object):
    def __init__(self, message: str, id: int):
        self.id = id
        self.message = message

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return self.__str__()

    def save(self) -> str:
        return f'<s>{self.message}</s>\n'


class Corpus(object):
    def __init__(self, participant: str):
        self.participant = participant
        self.records = []

    def add(self, message: str, id: int = 0):
        self.records.append(Record(message, id))

    def save(self):
        with open(f'../out/{self.participant}.txt', 'w', encoding='utf-8') as fw:
            fw.writelines(list([rec.save() for rec in self.records]))
