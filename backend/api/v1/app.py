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


if __name__ == "__main__":
    app.run()