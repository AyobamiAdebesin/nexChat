#!/usr/bin/env python3
""" DataBase Storage """
import os
import MySQLdb
from dotenv import load_dotenv
from sqlalchemy.orm.exc import NoResultFound
from typing import Mapping, List, Any, Union

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

    def all(self, cls=None) -> Mapping[str, Any]:
        """ Query on the current database session all objects of the
            class name passed as argument """
        from backend.models.users import User
        from backend.models.channels import Channel
        from backend.models.messages import Message

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
        from backend.models.channels import Channel
        from backend.models.messages import Message
        from backend.models.users import User
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current database session obj if not None """
        if obj:
            self.__session.delete(obj)

    def delete_by_username(self, username):
        """ Delete a user by username """
        from backend.models.users import User
        try:
            user = self.find_user_by(username=username)
        except NoResultFound:
            return
        else:
            self.delete(user)
            self.save()

    def reload(self):
        """ Create all tables in the database and the current database session
            from the engine """
        from sqlalchemy.orm import sessionmaker, scoped_session
        from backend.models.channels import Channel
        from backend.models.messages import Message
        from backend.models.users import User
        from backend.models.base_model import BaseModel, Base

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

    def find_user_by(self, **kwargs):
        """ Find a user by a given attribute """
        from backend.models.users import User
        if kwargs:
            for user in self.all(User).values():
                for key, value in kwargs.items():
                    if getattr(user, key) == value:
                        return user
        raise NoResultFound

    def count(self, cls=None):
        """ Count the number of objects in storage """
        if cls:
            return len(self.all(cls))
        return len(self.all())

    def find_channel_by(self, from_user, to_user):
        """ Find a channel by a given attribute """
        from backend.models.channels import Channel
        # Search for a channel with the given users
        # The users can be in any order. From the perspective of
        # the database, the channel is the same regardless of the
        # order of the users
        try:
            channel = self.__session.query(Channel).filter_by(Channel.from_user.in_([from_user, to_user])) \
            .filter_by(Channel.to_user.in_([from_user, to_user])) \
            .first()
        except Exception():
            raise NoResultFound
        return channel
