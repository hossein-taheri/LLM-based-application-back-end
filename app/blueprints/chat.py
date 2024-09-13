from openai import OpenAI
from bson import ObjectId
from datetime import datetime
from app.models.chat import Chat, ChatMessage
from flask import Blueprint, jsonify, request
from app.middlewares.jwt_required import jwt_required

chat = Blueprint('chat', __name__)

client = OpenAI()


@chat.route('/list', methods=['GET'])
@jwt_required
def list_all_chats():
    try:
        user_id = ObjectId(request.user_id)
        chats = Chat.objects(user_id=user_id).only('id', 'created_at')
        chat_list = [{'chat_id': str(chat.id), 'created_at': chat.created_at} for chat in chats]
        return jsonify({'status': 'success', 'chats': chat_list}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@chat.route('/create', methods=['POST'])
@jwt_required
def create_chat():
    try:
        user_id = ObjectId(request.user_id)
        new_chat = Chat(
            user_id=user_id,
            messages=[],
            created_at=datetime.utcnow()
        )
        new_chat.save()
        return jsonify({'status': 'success', 'chat_id': str(new_chat.id)}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@chat.route('/send-message', methods=['POST'])
@jwt_required
def send_message():
    try:
        user_id = ObjectId(request.user_id)
        data = request.json
        chat_id = data.get('chat_id')
        message_text = data.get('message')

        if not chat_id or not message_text:
            return jsonify({'status': 'error', 'message': 'Missing chat_id or message'}), 400

        chat = Chat.objects(id=ObjectId(chat_id), user_id=user_id).first()

        if not chat or str(chat.user_id) != str(user_id):
            return jsonify({'status': 'error', 'message': 'Chat not found'}), 404

        new_message = ChatMessage(
            text=message_text,
            is_users=True,
            created_at=datetime.utcnow()
        )

        chat.messages.append(new_message)
        chat.save()

        previous_messages = [
            {
                'role': 'system' if msg.is_systems else 'user' if msg.is_users else 'assistant', 'content': msg.text
            } for msg in chat.messages
        ]

        previous_messages.append({
            'role': 'user',
            'content': message_text
        })

        response = client.chat.completions.create(
            model="ft:gpt-4o-mini-2024-07-18:personal::9zIBverq",
            messages=previous_messages,
        )

        gpt_reply = response.choices[0].message.content
        print("gpt_reply", gpt_reply)
        gpt_message = ChatMessage(
            text=gpt_reply,
            is_users=False,
            created_at=datetime.utcnow()
        )
        chat.messages.append(gpt_message)
        chat.save()

        return jsonify({
            'status': 'success',
            'message': 'Message sent successfully',
            'data': {
                'text': gpt_message.text,
                'is_users': False,
                'created_at': gpt_message.created_at
            }
        }), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@chat.route('/get-all-messages', methods=['GET'])
@jwt_required
def get_all_messages():
    try:
        user_id = ObjectId(request.user_id)
        chat_id = request.args.get('chat_id')

        if not chat_id:
            return jsonify({'status': 'error', 'message': 'Missing chat_id'}), 400

        chat = Chat.objects(id=ObjectId(chat_id), user_id=user_id).first()

        if not chat or str(chat.user_id) != str(user_id):
            return jsonify({'status': 'error', 'message': 'Chat not found'}), 404

        messages = [{
            'text': message.text,
            'is_users': message.is_users,
            'created_at': message.created_at
        } for message in chat.messages]

        return jsonify({'status': 'success', 'messages': messages}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
