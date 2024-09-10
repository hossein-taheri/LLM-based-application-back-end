import os

import jwt
from app.models.user import User
from mongoengine import NotUniqueError
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request

auth = Blueprint('auth', __name__)

SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
print(SECRET_KEY)


def generate_token(user_id, exp_minutes=60):
    """Generate a JWT token."""
    exp = datetime.utcnow() + timedelta(minutes=exp_minutes)
    token = jwt.encode({'user_id': str(user_id), 'exp': exp}, SECRET_KEY, algorithm='HS256')
    return token


@auth.route('/sign-up', methods=['POST'])
def sign_up():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    password_hash, salt = User.hash_password(password)

    user = User(email=email, password_hash=password_hash, salt=salt, created_at=datetime.utcnow())

    try:
        user.save()
    except NotUniqueError:
        return jsonify({'error': 'Email already exists'}), 400

    return jsonify({'message': 'User created successfully'}), 201


@auth.route('/sign-in', methods=['POST'])
def sign_in():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.objects(email=email).first()

    if not user:
        return jsonify({'error': 'Invalid email or password'}), 400

    if not User.check_password(password, user.password_hash, user.salt):
        return jsonify({'error': 'Invalid email or password'}), 400

    access_token = generate_token(user.id)

    return jsonify({
        'message': 'Signed in successfully',
        'data': {
            'access-token': access_token,
        }
    }), 200


@auth.route('/verify-email', methods=['POST'])
def verify_email():
    return jsonify({'message': 'Email verification logic goes here'}), 200
