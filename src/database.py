#!/usr/bin/env python3
# wykys 2020
# databáze konverzací pro generování korpusu

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr, declarative_base
from sqlalchemy import Column, Integer, Unicode, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from uuid import uuid4


def new_id():
    return uuid4().int


@as_declarative()
class BaseModel(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)


class Message(BaseModel):
    text = Column(Unicode)
    datetime = Column(DateTime)

    chat = relationship('Chat')
    participant = relationship('Participant')

    chat_id = Column(Integer, ForeignKey('chat.id'))
    participant_id = Column(Integer, ForeignKey('participant.id'))

    def __repr__(self):
        return f'Message: {self.text}'


class Participant(BaseModel):
    name = Column(Unicode, unique=True)
    messages = relationship(Message, backref='participant_message')
    chats = relationship('Chat', secondary='link')

    def get_cnt_chats(self):
        return len(self.chats)

    def get_cnt_messages(self):
        return len(self.messages)

    def __repr__(self):
        return f'Participant: {self.name}'


class Chat(BaseModel):
    messages = relationship(Message, backref='chat_messege')
    participants = relationship(Participant, secondary='link')

    def get_cnt_messages(self):
        return len(self.messages)

    def get_cnt_participants(self):
        return len(self.participants)

    def __repr__(self):
        return f'Chat: {self.id}'


class Link(BaseModel):
    chat_id = Column(Integer, ForeignKey('chat.id'))
    participant_id = Column(Integer, ForeignKey('participant.id'))

    chat = relationship(Chat, backref=backref('link', cascade='all, delete-orphan'))
    participant = relationship(Participant, backref=backref('link', cascade='all, delete-orphan'))

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }


class Db(object):
    def __init__(self):
        #engine = create_engine(f'sqlite:///:memory:', echo=False)
        engine = create_engine(f'sqlite:///test.db', echo=False)
        _session = sessionmaker(bind=engine)
        self.session = _session()
        BaseModel.metadata.create_all(engine)

    def query(self, param):
        return self.session.query(param)

    def get_chats(self):
        return self.query(Chat)

    def get_participants(self):
        return self.query(Participant)

    def get_messages(self):
        return self.query(Message)

    def get_participant(self, name: str):
        return self.query(Participant).filter_by(name=name).first()

    def new_chat(self):
        return Chat()

    def new_participant(self):
        return Participant()

    def new_message(self):
        return Message()

    def add(self, item):
        self.session.add(item)

    def commit(self):
        self.session.flush()
        self.session.commit()

    def delete(self, item):
        self.session.delete(item)


db = Db()

if __name__ == '__main__':
    participant = Participant(name='Karel Vočko')
    chat = Chat()
    message = Message(participant=participant, chat=chat, text='Ahoj světe')

    participant.chats.append(chat)
    chat.participants.append(participant)

    db.add(chat)
    db.add(participant)
    db.add(message)

    db.commit()

    query = db.query(Participant).first()
    print(query.chats)

    print(db.get_participant('Petr'))

    print(db.query(Chat).first().participants)
