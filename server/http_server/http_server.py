import uuid

from flask import Flask, jsonify, request
from uuid import UUID

from auxiliary.message import Message
from server.services.user_service import UserService
from server.services.message_service import MessageService
from server.services.conversation_service import ConversationService
from server.connection_manager import ConnectionManager
from server.utils import model_to_dict
app = Flask(__name__)

user_service: UserService = None
message_service: MessageService = None
conversation_service: ConversationService = None
connection_manager = ConnectionManager()

@app.get('/users')
def get_users():
    users = user_service.get_users()
    return users
    # Convert list of User objects to list of dicts
    return jsonify([model_to_dict(u) for u in users])


@app.get('/users/<user_id>')
def get_user(user_id):
    user = user_service.get_user_by_id(user_id)
    if user:
        return jsonify(model_to_dict(user))
    return jsonify({"error": "User not found"}), 404


@app.post('/users/register')
def register():
    if not "socket_id" in request.form:
        return jsonify({"error": "Socket Id was not provided"}), 400

    username = request.form.get('username')
    password = request.form.get('password')
    socket_id = UUID(request.form.get('socket_id'))

    user_id = user_service.create_user(username)

    success = connection_manager.promote_connection(socket_id, user_id)
    if success:
        return jsonify({
            "message": "Register successful",
            "user_id": user_id
        }), 200
    else:
        # This happens if the socket disconnected before login
        return jsonify({"error": "Socket connection invalid"}), 400


@app.post('/users/login')
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    socket_id = UUID(request.form.get('socket_id'))

    user = user_service.get_user_by_username(username)

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    success = connection_manager.promote_connection(socket_id, user.id)

    if not success:
        return jsonify({"error": "Socket connection invalid"}), 400

    user_conversations = conversation_service.get_conversations_by_user_id(user.id)

    conversations_ids = [conversation['conversation_id'] for conversation in user_conversations]
    connection_manager.bulk_join_rooms(user.id, conversations_ids)

    return jsonify({
        "message": "Login successful",
        "user_id": user.id
    }), 200

@app.get('/messages/<conversation_id>')
def get_conversation_messages(conversation_id):
    messages = message_service.get_messages_by_conversation_id(conversation_id)
    return jsonify(messages)

@app.get('/conversations/<user_id>')
def get_user_conversations(user_id):
    conversations = conversation_service.get_conversations_by_user_id(uuid.UUID(user_id))
    return jsonify(conversations)

@app.post('/conversations')
def create_conversation():
    conversation = request.get_json()
    name = conversation.get('name')
    type = conversation.get('type')
    memberIds = conversation.get('members')
    conversation = conversation_service.create_conversation(type, memberIds, name)

    for member_id in memberIds:
        connection_manager.join_room(
            user_id=uuid.UUID(member_id),
            conversation_id=conversation['id']
        )

    return jsonify(conversation)

def run_http_server(host, port):
    global user_service, message_service, conversation_service
    user_service = UserService()
    message_service = MessageService()
    conversation_service = ConversationService()

    app.run(host=host, port=port, debug=False, use_reloader=False)