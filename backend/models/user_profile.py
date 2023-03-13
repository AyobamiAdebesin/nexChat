#!/usr/bin/env python3
""" User Profile model """
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base


class UserProfile(BaseModel, Base):
    """ Defines a user profile for a user """
    __tablename__ = 'user_profile'
    user_id = Column(String(128), ForeignKey('users.id'), nullable=False)