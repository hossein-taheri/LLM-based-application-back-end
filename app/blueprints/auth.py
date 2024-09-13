import os
import jwt
from app.models.user import User
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from app.models.forgot_password_token import ForgotPasswordToken

from app.services.email_service import send_verification_email, send_forgot_password

auth = Blueprint('auth', __name__)

SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')


def generate_token(user_id, exp_minutes=60):
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

    verification_token = User.generate_token()

    user = User(
        email=email,
        verification_token=verification_token,
        password_hash=password_hash,
        salt=salt,
        created_at=datetime.utcnow()
    )

    old_user = User.objects(email=email).first()
    if old_user is not None:
        if old_user.verified_email_at is not None:
            return jsonify({'error': 'Email already exists'}), 400
        else:
            old_user.delete()

    send_verification_email(
        email,
        verification_token
    )

    user.save()
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

    if user.verified_email_at is None:
        return jsonify({'error': 'Please verify your email first.'}), 400

    access_token = generate_token(user.id)

    return jsonify({
        'message': 'Signed in successfully',
        'data': {
            'access-token': access_token,
        }
    }), 200


@auth.route('/verify-email/<token>', methods=['POST'])
def verify_email(token):
    user = User.objects(verification_token=token).first()

    if not user:
        return jsonify({'error': 'Invalid or expired token'}), 400

    if user.verified_email_at:
        return jsonify({'message': 'Email already verified'}), 200

    user.verified_email_at = datetime.utcnow()
    user.save()

    return jsonify({'message': 'Email verified successfully'}), 200


@auth.route('/forgot-password', methods=['POST'])
def forgot_password_request():
    data = request.get_json()
    user_email = data.get('email')

    user = User.objects(email=user_email).first()
    if not user:
        return jsonify({'error': 'User with this email does not exist'}), 404

    forgot_password_token = User.generate_token()

    expires_at = datetime.utcnow() + timedelta(minutes=15)
    forgot_password_token = ForgotPasswordToken(user=user, token=forgot_password_token, expires_at=expires_at)
    forgot_password_token.save()

    send_forgot_password(
        user_email,
        forgot_password_token.token
    )

    return jsonify({'message': 'Forgot password email sent'}), 200


@auth.route('/forgot-password/change-password', methods=['POST'])
def forgot_password_change():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')

    forgot_password_entry = ForgotPasswordToken.objects(token=token).first()

    if not forgot_password_entry or forgot_password_entry.expires_at < datetime.utcnow():
        return jsonify({'error': 'Invalid or expired token'}), 400

    user = forgot_password_entry.user
    password_hash, salt = User.hash_password(new_password)
    user.password_hash = password_hash
    user.salt = salt
    user.save()

    forgot_password_entry.delete()

    return jsonify({'message': 'Password reset successfully'}), 200
