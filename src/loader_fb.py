#!/usr/bin/env python3
# wykys 2020
# program pro vytváření korpusů z Facebook JSON

import json
from datetime import datetime
from loader_prototype import LoaderPrototype
from database import db


class FbLoader(LoaderPrototype):
    def __init__(self, path='../data/message_1.json'):
        super().__init__(path)

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
            self.data = json.load(fr, object_hook=fix_fb_code)

    def decode(self):
        chat = db.Chat()
        chat.selected = False

        participants_dict = dict()
        for p in db.get_participants():
            participants_dict[p.name] = p

        for p in self.data['participants']:
            if 'name' in p:
                name = p['name']
                if not name in participants_dict:
                    participant = db.Participant()
                    participant.name = name
                    chat.participants.append(participant)
                    participants_dict[name] = participant

        for message in self.data['messages']:
            if 'content' in message and 'sender_name' in message and 'timestamp_ms' in message:

                # blocked user
                if not name in participants_dict:
                    participant = db.Participant()
                    participant.name = name
                    chat.participants.append(participant)
                    participants_dict[name] = participant

                msg = db.Message()
                msg.participant = participants_dict[name]
                msg.text = message['content']
                msg.datetime = datetime.fromtimestamp(int(message['timestamp_ms']) / 1000)
                chat.messages.append(msg)

        db.add(chat)
        for name, participant in participants_dict.items():
            db.add(participant)
        db.commit()


if __name__ == '__main__':
    loader = FbLoader()
