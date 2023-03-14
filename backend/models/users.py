#!/usr/bin/env python3
""" User Model """
import pusher
from backend.models.base_model import BaseModel, Base
from uuid import uuid4
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """ Defines a user in the app """
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    username = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
