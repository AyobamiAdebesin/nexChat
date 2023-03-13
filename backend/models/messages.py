#!/usr/bin/env python3
""" Messages Model """
import pusher
from backend.models.base_model import BaseModel, Base
from uuid import uuid4
from sqlalchemy import Column, Text, String, ForeignKey
from sqlalchemy.orm import relationship


class Message(BaseModel, Base):
    """ Defines a message object in the app """
    __tablename__ = 'messages'
    message = Column(Text(), nullable=False)
    from_user = Column(String(128), ForeignKey('users.id'), nullable=False)
    to_user = Column(String(128), ForeignKey('users.id'), nullable=False)
    channel_id = Column(String(128), nullable=False)
