#!/usr/bin/env python3
""" Entry point for backend """
import flask
import os
#import dotenv
import pusher
from flask import Flask, request, jsonify
from models.engine.db_storage import DBStorage
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


@app.route('/')
def index():
    """ Index route """
    return jsonify('Hello World')


@app.route('/api/v1/register', methods=['POST'])
def register():
    """ Register route """
    data = request.get_json()
    username = data['username']
    password = generate_password_hash(data['password'])
    
    try:
        user = User(username=username, password=password)
        storage.new(user)
        storage.save()
    except:
        return jsonify({'error': 'User already exists'}), 400
    return jsonify({'success': 'User created'}), 201

@app.route('/login')


@app.teardown_appcontext
def teardown_appcontext(exception):
    """ Closes the storage on teardown """
    storage.close()


if __name__ == "__main__":
    app.run()
