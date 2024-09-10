from flask import Blueprint, jsonify, request

from app.middleware.jwt_required import jwt_required

chat = Blueprint('chat', __name__)


@chat.route('/create', methods=['POST'])
@jwt_required
def create_chat():
    return request.user_id


@chat.route('/list', methods=['GET'])
def list_chat():
    pass


@chat.route('/send-message', methods=['POST'])
def send_message():
    pass


@chat.route('/get-all-messages', methods=['POST'])
def get_all_messages():
    pass
