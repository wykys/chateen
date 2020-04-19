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


class CorpusDict(object):
    def __init__(self):
        self.corpus = dict()

    def add(self, participant: str, message: str, id: int = 0):
        if not participant in self.corpus:
            self.corpus[participant] = Corpus(participant)
        self.corpus[participant].add(message, id)

    def save(self):
        for participant in self.corpus:
            self.corpus[participant].save()

    def show(self):
        for participant in self.corpus:
            for rec in self.corpus[participant].records:
                print(rec.id)

    def get_participants_from_chat(self, id: int) -> list:
        res = []
        for participant in self.corpus:
            for rec in self.corpus[participant].records:
                if rec.id == id:
                    res.append(participant)
                    break
        return res


    def get_top_id(self):
        tmp = dict()
        for participant in self.corpus:
            for rec in self.corpus[participant].records:
                id = str(rec.id)
                if not id in tmp:
                    tmp[id] = 1
                else:
                    tmp[id] += 1
        count = 0
        id = ''
        for key in tmp:
            if tmp[key] > count:
                count = tmp[key]
                id = key
        print(id, count)
        return int(id)

    def get_chat_with_id(self, id: int):
        for participant in self.corpus:
            for rec in self.corpus[participant].records:
                if id == rec.id:
                    print(participant, rec.message)
