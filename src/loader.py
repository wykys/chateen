from loader_fb import FbLoader
from loader_ig import IgLoader
from pathlib import Path
import json


class Loader(object):
    def __init__(self, path, callback_progress=None):
        self.path = path
        if self.open_json(path):
            self.load_json_to_database(callback_progress)

    def open_json(self, path):
        p = Path(self.path)
        if p.is_file():
            self.path = path
            with open(self.path, 'r', encoding='utf-8') as fr:
                self.json = json.load(fr)
            return True
        return False

    def load_json_to_database(self, callback_progress):
        if type(self.json) is dict:
            FbLoader(self.path, callback_progress)
        elif type(self.json) is list:
            IgLoader(self.path, callback_progress)
