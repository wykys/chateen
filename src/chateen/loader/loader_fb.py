#!/usr/bin/env python3
# wykys 2020
# program pro vytváření korpusů z Facebook JSON

import json
from datetime import datetime
from ..database import db
from .loader_prototype import LoaderPrototype


class FbLoader(LoaderPrototype):
    def __init__(self, path='../data/message_1.json', callback_progress=None):
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
        self.progress(0)

        chat = db.Chat()
        chat.selected = False

        participants_dict = dict()
        for p in db.get_participants():
            participants_dict[p.name] = p

        number_of_messages = 0
        for message in self.data['messages']:
            if 'content' in message and 'sender_name' in message and 'timestamp_ms' in message:
                number_of_messages += 1

        for p in self.data['participants']:
            if 'name' in p:
                name = p['name']
                if not name in participants_dict:
                    participant = db.Participant()
                    participant.name = name
                    chat.participants.append(participant)
                    participants_dict[name] = participant
                    print(name)

        messages_counter = 0
        for message in self.data['messages']:
            if 'content' in message and 'sender_name' in message and 'timestamp_ms' in message:

                name = message['sender_name']
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

                messages_counter += 1
                self.progress(100 * messages_counter / number_of_messages)

        db.add(chat)
        for name, participant in participants_dict.items():
            db.add(participant)
        db.commit()


if __name__ == '__main__':
    loader = FbLoader()
