# wykys 2020
# prototyp načítacího objektu

from pathlib import Path
from corpus import CorpusDict

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
