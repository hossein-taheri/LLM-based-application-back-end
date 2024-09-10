from flask import Blueprint, jsonify, request

auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods=['GET'])
def sign_up():
    return "sign up"


@auth.route('/sign-in', methods=['POST'])
def sign_in():
    pass


@auth.route('/verify-email', methods=['POST'])
def verify_email():
    pass
