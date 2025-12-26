from flask import Flask, jsonify, request
from uuid import UUID
from server.services.user_service import UserService
from server.services.message_service import MessageService
from server.connection_manager import ConnectionManager
app = Flask(__name__)

user_service: UserService = None
message_service: MessageService = None
connection_manager = ConnectionManager()


def model_to_dict(model):
    """Helper to convert SQLAlchemy models to dicts"""
    if not model:
        return None
    return {col.name: getattr(model, col.name) for col in model.__table__.columns}


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
    print('sexssadasd')
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

    if success:
        return jsonify({
            "message": "Login successful",
            "user_id": user.id
        }), 200
    else:
        # This happens if the socket disconnected before login
        return jsonify({"error": "Socket connection invalid"}), 400

@app.get('/messages/<sender_id>/<receiver_id>')
def get_conversation(sender_id, receiver_id):
    messages = message_service.get_messages_by_client_id(sender_id, receiver_id)
    return jsonify([model_to_dict(m) for m in messages])


def run_http_server(host, port):
    global user_service, message_service
    user_service = UserService()
    message_service = MessageService()

    app.run(host=host, port=port, debug=False, use_reloader=False)