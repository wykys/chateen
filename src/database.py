#!/usr/bin/env python3
# wykys 2020
# databáze konverzací pro generování korpusu

from sqlalchemy import create_engine, text, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr, declarative_base
from sqlalchemy import Column, Integer, Unicode, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from database_models import BaseModel, Chat, Participant, Message, Link
from database_reduce import DbReduce


class Db(object):
    def __init__(self):
        engine = create_engine(f'sqlite:///:memory:', echo=False)
        #engine = create_engine(f'sqlite:///test.db', echo=False)
        _session = sessionmaker(bind=engine)
        self.session = _session()
        BaseModel.metadata.create_all(engine)

        self.conn = engine.connect()
        self.execute = self.conn.execute
        self.text = text
        self.func = func

        self.query = self.session.query
        self.add = self.session.add
        self.commit = self.session.commit
        self.delete = self.session.delete

        self.Chat = Chat
        self.Link = Link
        self.Message = Message
        self.Participant = Participant

    def get_chats(self):
        return self.query(Chat)

    def get_participants(self):
        return self.query(Participant)

    def get_messages(self):
        return self.query(Message)

    def delete_all(self):
        self.__init__()

    def sql(self, cmd):
        return self.execute(text(
            cmd
        )).fetchall()

    def reduce(self):
        DbReduce(self)


db = Db()
