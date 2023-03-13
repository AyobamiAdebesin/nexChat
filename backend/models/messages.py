#!/usr/bin/env python3
""" Messages Model """
import pusher
from models.base_model import BaseModel, Base
from uuid import uuid4
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class Messages(BaseModel, Base):
    """ Defines a message object in the app """
    __tablename__ = 'messages'
    from_user = Column(String(128), nullable=False)
    to_user = Column(String(128), nullable=False)
    channel_id = Column(String(128), nullable=False)