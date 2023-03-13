#!/usr/bin/env python3
""" Entry point for backend """
import flask
import os
#import dotenv
import pusher
from backend.models import storage
from flask import Flask, request, jsonify
from backend.models.users import User
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


@app.route('/')
def index():
    """ Index route """
    return jsonify('Hello World')


@app.route('/api/v1/register', methods=['POST'], strict_slashes=False)
def register():
    """ Register route """
    username = request.form.get('username')
    password = request.form.get('password')
    
    try:
        storage.find_user_by(username=username)
    except NoResultFound:
        user = User(username=username, password=generate_password_hash(password))
        user.save()
        return jsonify({'success': 'User created'}), 201
    else:
        return jsonify({'error': 'User already exists'}), 400
        


@app.teardown_appcontext
def teardown_appcontext(exception):
    """ Closes the storage on teardown """
    storage.close()


if __name__ == "__main__":
    app.run()
