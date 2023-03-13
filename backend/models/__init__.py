#!/usr/bin/env python3
""" Endpoint for abstracted database """
import os
from backend.models.base_model import BaseModel, Base
from backend.models.channels import Channel
from backend.models.messages import Message
from backend.models.users import User
from backend.models.engine.db_storage import DBStorage

storage = DBStorage()
storage.reload()
