#!/usr/bin/env python3
""" Base Model """
import os
import pusher
import sys
import uuid
from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Text, Table, MetaData


Base = declarative_base()

class BaseModel:
    """ Base Model """
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime(timezone=False), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=False), nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """ Initializes model """
        if kwargs is None:
            # If kwargs is None, then we are creating a new instance
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        elif '__class__' in kwargs:
            # If kwargs is not None and does not contain the '__class__' key,
            # then we are creating an instance from a dictionary
            # passed into the constructor. We update the 'updated_at' and 'created_at'
            # attributes to be datetime objects instead of strings.
            kwargs['updated_at'] = datetime().strptime(kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime().strptime(kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')

            del kwargs['__class__']
            self.__dict__.update(kwargs)
        else:
            self.id = str((uuid4()))
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            self.__dict__.update(kwargs)
    
    def __str__(self):
        """ Return string representation """
        dictionary = {}
        dictionary.update(self.__dict__)
        if '_sa_instance_state' in dictionary.keys():
            del dictionary['_sa_instance_state']
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, dictionary)

    def save(self):
        """ Updates 'updated_at' with current time when instance is changed """
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dictionary.keys():
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        """Delete an instance"""
        from models import storage
        storage.delete(self)
