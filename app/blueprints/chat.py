from flask import Blueprint, jsonify, request

chat = Blueprint('chat', __name__)

@chat.route('/create', methods=['POST'])
def create_chat():
    pass


@chat.route('/list', methods=['GET'])
def list_chat():
    pass


@chat.route('/send-message', methods=['POST'])
def send_message():
    pass


@chat.route('/get-all-messages', methods=['POST'])
def get_all_messages():
    pass
