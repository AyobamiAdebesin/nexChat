#!/usr/bin/env python3
""" Entry point for backend """
import flask
import os
import dotenv
from dotenv import load_dotenv
import pusher
from backend.models import storage
from flask import Flask, request, jsonify
from backend.models.users import User
from sqlalchemy.orm.exc import NoResultFound
from backend.models.channels import Channel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('TWIBBLY_JWT_SECRET')
jwt = JWTManager(app)

# Pusher setup
pusher = pusher.Pusher(
    app_id=os.getenv('TWIBBLY_PUSHER_APP_ID'),
    key=os.getenv('TWIBBLY_PUSHER_KEY'),
    secret=os.getenv('TWIBBLY_PUSHER_SECRET'),
    cluster=os.getenv('TWIBBLY_PUSHER_CLUSTER'),
    ssl=True)


@app.route('/', strict_slashes=False, methods=['GET'])
def index():
    """ Index route """
    return jsonify('Hello World')


@app.route('/api/v1/register', methods=['POST'], strict_slashes=False)
def register():
    """ Register route """
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    try:
        storage.find_user_by(username=username)
    except NoResultFound:
        user = User(username=username,
                    password=generate_password_hash(password), email=email)
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

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.


@app.route("/api/v1/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


# Generate channel
@app.route('/api/v1/request_chat', methods=['POST'], strict_slashes=False)
@jwt_required()
def request_chat():
    """ Generates a channel for two users """
    from_user = request.form.get('from_user', '')
    to_user = request.form.get('to_user', '')
    to_user_channel = f"private-notification_user_{to_user}"
    from_user_channel = f"private-notification_user_{from_user}"

    # Check if a channel already exists between the two users
    channel = storage.find_channel_by(from_user=from_user, to_user=to_user)
    if channel is None:
        channel_name = f"private-chat_{from_user}_{to_user}"
        new_channel = Channel(
            name=channel_name, from_user=from_user, to_user=to_user)
        new_channel.save()
    else:
        channel_name = channel.name
    data = {
        "from_user": from_user,
        "to_user": to_user,
        "from_user_notification_channel": from_user_channel,
        "to_user_notification_channel": to_user_channel,
        "channel_name": channel_name
    }

    # Trigger an event on the to_user's notification channel
    pusher.trigger(to_user_channel, 'new_chat', data)
    return jsonify({
        'status': 'success',
        'message': 'Channel created',
        'data': data
    }), 201


@app.route('/api/v1/pusher/auth', methods=['POST'], strict_slashes=False)
@jwt_required()
def pusher_authentication():
    """ Pusher authentication route """
    auth_handler = pusher.authenticate(
        channel=request.form['channel_name'],
        socket_id=request.form['socket_id']
    )
    return jsonify(auth_handler)


@app.route('/api/v1/send_message', methods=['POST'], strict_slashes=False)
@jwt_required()
def send_message():
    """ Sends a message to a channel """
    from_user = request.form.get('from_user', '')
    to_user = request.form.get('to_user', '')
    message = request.form.get('message', '')
    channel_name = request.form.get('channel_name', '')

    # Save the message to the database
    new_message = Message()
    new_message.from_user = from_user
    new_message.to_user = to_user
    new_message.message = message
    new_message.channel_id = channel_name
    new_message.save()

    message = {
        'from_user': from_user,
        'to_user': to_user,
        'message': message,
        'channel_name': channel_name
    }
    pusher.trigger(channel_name, 'new_message', message)
    return jsonify({
        'status': 'success',
        'message': 'Message sent'
    }), 200

    # channel_name = request.form.get('channel_name')
    # message = request.form.get('message')
    # username = get_jwt_identity()
    # data = {
    #     'username': username,
    #     'message': message
    # }
    # pusher.trigger(channel_name, 'new_message', data)


@app.route('/api/v1/users', methods=['GET'])
@jwt_required()
def get_users():
    """ Returns all users """
    users = storage.all(User).values()
    return jsonify([{"id": user.id, "username": user.username} for user in users]), 200


@app.route('/api/v1/get_message/<channel_name>', methods=['GET'])
@jwt_required()
def user_messages(channel_name):
    """ Returns all messages in a channel """
    messages = storage.find_messages_by(channel_id=channel_name)
    return jsonify([{
        'from_user': message.from_user,
        'to_user': message.to_user,
        'message': message.message,
        'channel_name': message.channel_id
    } for message in messages]), 200


@app.teardown_appcontext
def teardown_appcontext(exception):
    """ Closes the storage on teardown """
    storage.close()


if __name__ == "__main__":
    app.run(debug=True)
