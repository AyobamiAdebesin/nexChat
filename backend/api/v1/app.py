#!/usr/bin/env python3
""" Entry point for backend """
import flask
import os
import dotenv
import pusher
from backend.models import storage
from flask import Flask, request, jsonify
from backend.models.users import User
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager 
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('TWIBBLY_JWT_SECRET')
jwt = JWTManager(app)


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
        user = User(username=username,
                    password=generate_password_hash(password))
        user.save()
        return jsonify({'success': 'User created'}), 201
    else:
        return jsonify({'error': 'User already exists'}), 400


@app.route('/api/v1/login', methods=['POST'], strict_slashes=False)
def login():
    """ Logs in a user """
    username = request.form.get('username')
    password = request.form.get('password')

    try:
        user = storage.find_user_by(username=username)
    except NoResultFound:
        return jsonify({'error': 'User not found'}), 404
    else:
        if check_password_hash(user.password, password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({'error': 'Invalid password'}), 401

#Protect a route with jwt_required, which will kick out requests
#without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

 
@app.teardown_appcontext
def teardown_appcontext(exception):
    """ Closes the storage on teardown """
    storage.close()


if __name__ == "__main__":
    app.run(debug=True)
