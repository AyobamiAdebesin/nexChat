#!/usr/bin/env python3
""" Endpoint for abstracted database """
import os
from models.base_model import BaseModel, Base
from models.channels import Channel
from models.messages import Message
from models.users import User
from models.engine.db_storage import DBStorage

storage = DBStorage()
storage.reload()
