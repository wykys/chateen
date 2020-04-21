#!/usr/bin/env python3
# wykys 2020
# program pro vytváření korpusů z Instagramu JSON

import json
from database import db
from loader_prototype import LoaderPrototype
from datetime import datetime


class IgLoader(LoaderPrototype):
    def __init__(self, path='../data/messages.json'):
        super().__init__(path)

    def load(self):
        with open(self.path, 'r', encoding='utf-8') as fr:
            self.data = json.load(fr)

    def decode(self):

        for data in self.data:
            if 'participants' in data and 'conversation' in data:
                chat = db.new_chat()
                db.add(chat)
                db.commit()

                for name in data['participants']:
                    participant = db.get_participant(name)
                    if name == '__karin_kaa_':
                        print('TUUU v participants')
                        print(participant)

                    if participant is None:
                        participant = db.new_participant()
                        participant.name = name
                        participant.chats.append(chat)
                        chat.participants.append(participant)
                        db.add(participant)
                        db.commit()
                    else:
                        participant.chats.append(chat)
                        chat.participants.append(participant)
                        db.commit()

                for message in data['conversation']:
                    if 'text' in message and 'sender' in message:
                        participant = db.get_participant(message['sender'])
                        # blocked user
                        if participant is None:
                            participant = db.new_participant()
                            participant.name = message['sender']
                            participant.chats.append(chat)
                            chat.participants.append(participant)
                            db.add(participant)
                            db.commit()

                        msg = db.new_message()
                        msg.chat = chat
                        msg.participant = participant
                        msg.text = message['text']
                        msg.datetime = datetime.fromisoformat(message['created_at'])
                        db.add(msg)
                        db.commit()


if __name__ == '__main__':
    loader = IgLoader()
