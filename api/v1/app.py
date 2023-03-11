#!/usr/bin/env python3
""" Entry point for twibbly app """
import os
import pusher
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/')
def index():
    """ Return index page """
    return jsonify("Pong")


if __name__ == "__main__":
    app.run()
