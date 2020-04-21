#!/usr/bin/env python3
# wykys 2020
# knihovna pro práci s korpusem

from database import db, Link

FAKE_NAME = 'Fejkař Otto'


class Corpus(object):
    def __init__(self):
        self.set_fake_user()
        self.clean_inactive_participants()
        self.clean_inactive_chats()

    def set_fake_user(self):
        self.fake_user = db.get_participant(FAKE_NAME)
        if self.fake_user is None:
            self.fake_user = db.new_participant()
            self.fake_user.name = FAKE_NAME
            db.add(self.fake_user)
            db.commit()

    def clean_inactive_participants(self, trasehold=50):
        inactive = [p for p in db.get_participants() if p.get_cnt_messages() < trasehold]
        for participant in inactive:
            if participant.name == FAKE_NAME:
                continue

            if len(participant.messages) > 0:
                for messages in participant.messages:
                    messages.participant = self.fake_user
                    db.commit()

                    if not messages.chat in self.fake_user.chats:
                        self.fake_user.chats.append(messages.chat)
                        messages.chat.participants.append(self.fake_user)
                        db.commit()

            participant.messages = []
            db.commit()

            for chat in participant.chats:

                link = db.query(Link).filter(
                    Link.participant_id == participant.id, Link.chat_id == chat.id
                ).first()

                if not link is None:
                    db.delete(link)
                    db.commit()

            db.delete(participant)
            db.commit()

    def clean_inactive_chats(self, trasehold=100):
        inactive = [c for c in db.get_chats() if c.get_cnt_messages() < trasehold]

        if len(inactive) > 1:
            fake_chat = inactive[0]

        for chat in inactive:
            if chat.id == fake_chat.id:
                continue

            for message in chat.messages:
                message.chat = fake_chat
                db.commit()

            for participant in chat.participants:
                if not fake_chat in participant.chats:
                    participant.chats.append(fake_chat)
                    fake_chat.participants.append(participant)
                    db.commit()

                    link = db.query(Link).filter(
                        Link.participant_id == participant.id, Link.chat_id == chat.id
                    ).first()
                    db.delete(link)
                    db.commit()

            db.delete(chat)
            db.commit()


if __name__ == '__main__':
    Corpus()
