#!/usr/bin/env python3
# wykys 2020
# program pro vytváření korpusů z Facebook JSON

import json
from corpus import Corpus


class FbLoader(object):
    def __init__(self, path='../data/message_1.json'):
        self.path = path
        self.load()
        self.decode()

    def load(self):
        def fix_fb_code(obj):
            def fix(s: str) -> str:
                return s.encode('latin_1').decode('utf-8')

            for key in obj:
                if isinstance(obj[key], str):
                    obj[key] = fix(obj[key])
                elif isinstance(obj[key], list):
                    obj[key] = list(
                        map(
                            lambda x:
                                fix(x) if isinstance(x, str) else x,
                                obj[key]
                        )
                    )
            return obj

        with open(self.path, 'r', encoding='utf-8') as fr:
            data = json.load(fr, object_hook=fix_fb_code)

        self.chat = data['messages']
        self.authors = tuple(map(lambda x: x['name'], data['participants']))
        self.corpus = dict()
        for author in self.authors:
            self.corpus[author] = Corpus(author)

    def decode(self):
        for message in self.chat:
            if 'content' in message and 'sender_name' in message:
                self.corpus[message['sender_name']].add(message['content'])

    def save(self):
        for name in self.corpus:
            self.corpus[name].save()


if __name__ == '__main__':
    loader = FbLoader()
    loader.save()
