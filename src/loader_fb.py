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
        chat = db.new_chat()
        db.add(chat)
        db.commit()

        for p in self.data['participants']:
            if 'name' in p:
                participant = db.new_participant()
                participant.name = p['name']
                participant.chats.append(chat)
                chat.participants.append(participant)
                db.add(participant)
                db.commit()

        for message in self.data['messages']:
            if 'content' in message and 'sender_name' in message and 'timestamp_ms' in message:
                participant = db.get_participant(message['sender_name'])
                msg = db.new_message()
                msg.chat = chat
                msg.participant = participant
                msg.text = message['content']
                time_stamp = int(message['timestamp_ms']) / 1000
                msg.datetime = datetime.fromtimestamp(time_stamp)
                db.add(msg)
                db.commit()


if __name__ == '__main__':
    loader = FbLoader()
