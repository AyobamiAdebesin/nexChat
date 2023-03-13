#!/usr/bin/env python3
""" DataBase Storage """
import os
import MySQLdb
from dotenv import load_dotenv


load_dotenv()


class DBStorage:
    """ Abstracts the Database layer and handles the storage of objects """
    __engine = None
    __session = None

    def __init__(self):
        """ Initialize the DBStorage class """
        from sqlalchemy import create_engine
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(os.getenv('TWIBBLY_MYSQL_USER'),
                                              os.getenv('TWIBBLY_MYSQL_PWD'),
                                              os.getenv('TWIBBLY_MYSQL_HOST'),
                                              os.getenv('TWIBBLY_MYSQL_DB')),
                                      pool_pre_ping=True)

    def all(self, cls=None):
        """ Query on the current database session all objects of the
            class name passed as argument """
        from models.users import User
        from models.channels import Channel
        from models.messages import Message

        classes = [User, Channel, Message]
        new_dict = {}
        if cls:
            for obj in self.__session.query(cls).all():
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                new_dict[key] = obj
        else:
            for cls in classes:
                for obj in self.__session.query(cls).all():
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """ Add the object to the current database session """
        from sqlalchemy.orm import sessionmaker
        from models.channels import Channel
        from models.messages import Message
        from models.users import User
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current database session obj if not None """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Create all tables in the database and the current database session
            from the engine """
        from sqlalchemy.orm import sessionmaker, scoped_session
        from models.channels import Channel
        from models.messages import Message
        from models.users import User
        from models.base_model import BaseModel, Base

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ Close the session """
        self.__session.close()

    def get(self, cls, id):
        """ Get an object by class and id """
        if cls and id:
            key = "{}.{}".format(cls, id)
            return self.all().get(key)
        return None

    def count(self, cls=None):
        """ Count the number of objects in storage """
        if cls:
            return len(self.all(cls))
        return len(self.all())
