#!/usr/bin/env python3
# wykys 2020
# ORL model databáze pro generování korpusu

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr, declarative_base
from sqlalchemy import Column, Integer, Unicode, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, backref


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
        return self.name


class Chat(BaseModel):
    selected = Column(Boolean)
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
