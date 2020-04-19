#!/usr/bin/env python3
# wykys 2020
# program pro vytváření korpusů z Instagramu JSON

import json
from corpus import Corpus
from loader_prototype import LoaderPrototype


class IgChat(object):
    def __init__(self, chat, id):
        self.id = id
        if 'participants' in chat and 'conversation' in chat:
            self.participants = chat['participants']
            self.conversation = chat['conversation']
        else:
            exit(1)


class IgLoader(LoaderPrototype):
    def __init__(self, path='../data/messages.json'):
        super().__init__(path)

    def load(self):
        with open(self.path, 'r', encoding='utf-8') as fr:
            data = json.load(fr)

        self.chat = []
        for id, chat in enumerate(data):
            self.chat.append(IgChat(chat, id))

    def decode(self):
        for chat in self.chat:
            for message in chat.conversation:
                if 'text' in message and 'sender' in message:
                    self.corpus.add(message['sender'], message['text'], chat.id)


if __name__ == '__main__':
    loader = IgLoader()
    loader.save()
