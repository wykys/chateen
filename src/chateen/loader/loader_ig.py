#!/usr/bin/env python3
# wykys 2020
# program pro vytváření korpusů z Instagramu JSON

import json
from datetime import datetime
from ..database import db
from .loader_prototype import LoaderPrototype

class IgLoader(LoaderPrototype):
    def __init__(self, path='../data/messages.json', callback_progress=None):
        super().__init__(path, callback_progress)

    def load(self):
        with open(self.path, 'r', encoding='utf-8') as fr:
            self.data = json.load(fr)

    def decode(self):
        self.progress(0)

        participants_dict = dict()
        for p in db.query(db.Participant):
            participants_dict[p.name] = p

        number_of_messages = 0
        for data in self.data:
            for message in data['conversation']:
                if 'text' in message and 'sender' in message:
                    number_of_messages += 1

        messages_counter = 0
        for data in self.data:
            if 'participants' in data and 'conversation' in data:
                chat = db.Chat()
                chat.selected = False

                for name in data['participants']:
                    if not name in participants_dict:
                        participant = db.Participant()
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
                            participant = db.Participant()
                            participant.name = name
                            chat.participants.append(participant)
                            participants_dict[name] = participant

                        elif not participants_dict[name] in chat.participants:
                            chat.participants.append(participants_dict[name])

                        msg = db.Message()
                        msg.participant = participants_dict[name]
                        msg.text = message['text']
                        msg.datetime = datetime.fromisoformat(message['created_at'])
                        chat.messages.append(msg)

                        messages_counter += 1
                        self.progress(100 * messages_counter / number_of_messages)

                db.add(chat)

            db.commit()


if __name__ == '__main__':
    loader = IgLoader()
