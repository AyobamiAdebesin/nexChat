#!/usr/bin/env python3
""" Entry point for backend """
import flask
import os
from flask import Flask, request, jsonify
import dotenv
import pusher


app = Flask(__name__)

@app.route('/')
def index():
    """ Index route """
    return jsonify('Hello World')

@app.route('/home')
def home():
    """ Return home page """
    return jsonify({'Hello': 'World'})

@app.teardown_appcontext
def teardown_appcontext(exception):
    """ Closes the storage on teardown """
    storage.close()


if __name__ == "__main__":
    app.run()