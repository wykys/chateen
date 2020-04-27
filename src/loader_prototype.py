# wykys 2020
# prototyp načítacího objektu

from pathlib import Path
from database import db

class LoaderPrototype(object):
    def __init__(self, path: str, callback_progress=None):
        self.callback_progress = callback_progress
        self.percent = None
        if self.set_path(path):
            self.load()
            self.decode()

    def set_path(self, path: str):
        p = Path(path)
        if p.is_file():
            self.path = path
            return True

        print(f'File {path} is not exist!')
        return False

    def load(self):
        print('Load is not defined')

    def decode(self):
        print('Decode is not defined')

    def progress(self, percent):
        percent = int(percent)
        if self.percent != percent:
            self.percent = percent
            if not self.callback_progress is None:
                self.callback_progress.emit(percent)
            else:
                print(f'\rProgress: {percent} %', end='')
                if percent == 100:
                    print()
