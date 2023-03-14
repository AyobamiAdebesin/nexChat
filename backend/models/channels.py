#!/usr/bin/env python3
""" Channels Model """
import pusher
from backend.models.base_model import BaseModel, Base
from uuid import uuid4
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Channel(BaseModel, Base):
    """ Defines a channel object in the app """
    __tablename__ = 'channels'
    name = Column(String(256), nullable=False)
    from_user = Column(String(128), ForeignKey('users.id'), nullable=False)
    to_user = Column(String(128), ForeignKey('users.id'), nullable=False)
