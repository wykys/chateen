#!/usr/bin/env python3
# wykys 2020
# databáze konverzací pro generování korpusu

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr, declarative_base
from sqlalchemy import Column, Integer, Unicode, ForeignKey
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
    time_stamp = Column(Integer)

    chat = relationship('Chat')
    participant = relationship('Participant')

    chat_id = Column(Integer, ForeignKey('chat.id'))
    participant_id = Column(Integer, ForeignKey('participant.id'))

    def __repr__(self):
        return f'Message: {self.text}'


class Participant(BaseModel):
    name = Column(Unicode)
    messages = relationship(Message, backref='participant_message')
    chats = relationship('Chat', secondary='link')

    def __repr__(self):
        return f'Participant: {self.name}'


class Chat(BaseModel):
    messages = relationship(Message, backref='chat_messege')
    participants = relationship(Participant, secondary='link')

    def __repr__(self):
        return f'Chat: {self.id}'


class Link(BaseModel):
    chat_id = Column(Integer, ForeignKey('chat.id'))
    participant_id = Column(Integer, ForeignKey('participant.id'))

    chat = relationship(Chat, backref=backref('link', cascade="all, delete-orphan"))
    participant = relationship(Participant, backref=backref('link', cascade="all, delete-orphan"))


if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:', echo=True)
    #engine = create_engine('sqlite:///test.db', echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    BaseModel.metadata.create_all(engine)

    participant = Participant(name='Karel Vočko')
    chat = Chat()
    message = Message(participant=participant, chat=chat, text='Ahoj světe')

    participant.chats.append(chat)
    chat.participants.append(participant)

    session.add(chat)
    session.add(participant)
    session.add(message)

    session.commit()

    query = session.query(Participant).first()
    print(query.chats)

    print(session.query(Chat).first().participants)
