# wykys 2020

from database_models import Link

FAKE_NAME = 'Fejkař Otto'


class DbReduce(object):
    def __init__(self, db):

        self.db = db

        self.set_fake_user()
        self.clean_inactive_participants()
        self.clean_inactive_chats()

    def set_fake_user(self):
        self.fake_user = self.db.get_participant(FAKE_NAME)
        if self.fake_user is None:
            self.fake_user = self.db.new_participant()
            self.fake_user.name = FAKE_NAME
            self.db.add(self.fake_user)
            self.db.commit()

    def clean_inactive_participants(self, trasehold=50):
        inactive = [p for p in self.db.get_participants() if p.get_cnt_messages() < trasehold]
        for participant in inactive:
            if participant.name == FAKE_NAME:
                continue

            if len(participant.messages) > 0:
                for messages in participant.messages:
                    messages.participant = self.fake_user
                    self.db.commit()

                    if not messages.chat in self.fake_user.chats:
                        self.fake_user.chats.append(messages.chat)
                        messages.chat.participants.append(self.fake_user)
                        self.db.commit()

            participant.messages = []
            self.db.commit()

            for chat in participant.chats:

                link = self.db.query(Link).filter(
                    Link.participant_id == participant.id, Link.chat_id == chat.id
                ).first()

                if not link is None:
                    self.db.delete(link)
                    self.db.commit()

            self.db.delete(participant)
            self.db.commit()

    def clean_inactive_chats(self, trasehold=100):
        inactive = [c for c in self.db.get_chats() if c.get_cnt_messages() < trasehold]

        if len(inactive) > 1:
            fake_chat = inactive[0]
        else:
            return

        for chat in inactive:
            if chat.id == fake_chat.id:
                continue

            for message in chat.messages:
                message.chat = fake_chat
                self.db.commit()

            for participant in chat.participants:
                if not fake_chat in participant.chats:
                    participant.chats.append(fake_chat)
                    fake_chat.participants.append(participant)
                    self.db.commit()

                    link = self.db.query(Link).filter(
                        Link.participant_id == participant.id, Link.chat_id == chat.id
                    ).first()
                    self.db.delete(link)
                    self.db.commit()

            self.db.delete(chat)
            self.db.commit()
