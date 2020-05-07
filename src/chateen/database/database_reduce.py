# wykys 2020

from .database_models import Link

FAKE_NAME = 'Fejkař Otto'


class DbReduce(object):
    def __init__(self, db):

        self.db = db
        self.set_fake_user()
        self.clean_inactive_participants()
        self.clean_inactive_chats()

    def sql_clean(self):
        trasehold = 50
        cmd = f"""
        with participants_with_enough_messages as (
            select p.id
            from participant p
                    inner join message m on p.id = m.participant_id
            group by p.id
            having count(m.id) < {trasehold}
        )
        update link
        set participant_id = {self.fake_user.id}
        where participant_id not in participants_with_enough_messages;
        """
        self.db.sql(cmd)

    def set_fake_user(self):
        db = self.db
        self.fake_user = db.get_participants().filter(db.Participant.name == FAKE_NAME).scalar()
        if self.fake_user is None:
            self.fake_user = self.db.Participant()
            self.fake_user.name = FAKE_NAME
            db.add(self.fake_user)
            db.commit()

    def clean_inactive_participants(self, trasehold=50):
        db = self.db
        inactive = db.get_participants().join(db.Message).group_by(
            db.Participant.id).having(db.func.count(db.Message.id) < trasehold).all()
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
                ).scalar()

                if not link is None:
                    db.delete(link)
                    db.commit()

            db.delete(participant)
            db.commit()

    def clean_inactive_chats(self, trasehold=100):
        db = self.db
        inactive = db.get_chats().join(db.Message).group_by(
            db.Chat.id).having(db.func.count(db.Message.id) < trasehold).all()

        if len(inactive) > 1:
            fake_chat = inactive[0]
        else:
            return

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
                    ).scalar()
                    db.delete(link)
                    db.commit()

            db.delete(chat)
            db.commit()
