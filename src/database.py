#!/usr/bin/env python3
# wykys 2020
# databáze konverzací pro generování korpusu

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr, declarative_base
from sqlalchemy import Column, Integer, Unicode, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from database_models import BaseModel, Chat, Participant, Message, Link
#from database_reduce import DbReduce


class Db(object):
    def __init__(self):
        engine = create_engine(f'sqlite:///:memory:', echo=False)
        #engine = create_engine(f'sqlite:///test.db', echo=False)
        _session = sessionmaker(bind=engine)
        self.session = _session()
        BaseModel.metadata.create_all(engine)

        self.query = self.session.query
        self.add = self.session.add
        self.commit = self.session.commit
        self.delete = self.session.delete

        self.new_chat = Chat
        self.new_link = Link
        self.new_message = Message
        self.new_participant = Participant

    def get_chats(self):
        return self.query(Chat)

    def get_participants(self):
        return self.query(Participant)

    def get_messages(self):
        return self.query(Message)

    def get_participant(self, name: str):
        return self.query(Participant).filter_by(name=name).first()

    def delete_all(self):
        self.__init__()

    def reduce(self):
        pass
        # DbReduce(self)


db = Db()
