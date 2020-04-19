# wykys 2020
# prototyp načítacího objektu

from pathlib import Path
from corpus import Corpus


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


class LoaderPrototype(object):
    def __init__(self, path: str):
        self.corpus = CorpusDict()
        self.authors = []
        self.set_path(path)
        self.load()
        self.decode()

    def set_path(self, path: str):
        p = Path(path)
        if p.is_file():
            self.path = path
        else:
            print(f'File {path} is not exist!')
            exit(1)

    def load(self):
        print('Load is not defined')
        pass

    def decode(self):
        print('Decode is not defined')
        pass

    def save(self):
        self.corpus.save()
