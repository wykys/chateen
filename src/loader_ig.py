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
        participants_dict = dict()
        for p in db.get_participants():
            participants_dict[p.name] = p

        for data in self.data:
            if 'participants' in data and 'conversation' in data:
                chat = db.new_chat()
                chat.selected = False

                for name in data['participants']:
                    if not name in participants_dict:
                        participant = db.new_participant()
                        participant.name = name
                        chat.participants.append(participant)
                        participants_dict[name] = participant
                    else:
                        chat.participants.append(participants_dict[name])

                for message in data['conversation']:
                    if 'text' in message and 'sender' in message:
                        name = message['sender']
                        # blocked user
                        if not name in participants_dict:
                            participant = db.new_participant()
                            participant.name = name
                            chat.participants.append(participant)
                            participants_dict[name] = participant

                        msg = db.new_message()
                        msg.participant = participants_dict[name]
                        msg.text = message['text']
                        msg.datetime = datetime.fromisoformat(message['created_at'])
                        chat.messages.append(msg)

                db.add(chat)

            for name, participant in participants_dict.items():
                db.add(participant)
            db.commit()


if __name__ == '__main__':
    loader = IgLoader()
