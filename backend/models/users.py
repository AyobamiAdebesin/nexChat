#!/usr/bin/env python3
""" User Model """
import pusher
from models.base_model import BaseModel, Base
from uuid import uuid4
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """ Defines a user in the app """
    __tablename__ = 'users'
    username = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    messages = relationship('Message', backref='users', cascade='all, delete')
    channels = relationship('Channel', backref='users', cascade='all, delete')
