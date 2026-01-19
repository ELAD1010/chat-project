import os
import atexit
import socket
import threading
import json
import asyncio
import requests
from dotenv import load_dotenv
from nicegui import ui, app
from auxiliary.message import Message
from client.config.app_config import AppConfig
from datetime import datetime
from client.ui.chat import initialize_ui, render_messages, select_chat as select_chat_action
from client.ui.app_state import chat_messages, selected_chat, current_user_id, CHATS
from client.ui.sidebar import render_chat_lists
from client import api


load_dotenv()

socket_id = None
app_config = AppConfig()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
is_shutting_down = False
main_loop = None

def connect_worker():
    global main_loop
    try:
        main_loop = asyncio.get_running_loop()
    except RuntimeError:
        pass
    threading.Thread(target=initialize_connection, daemon=True).start()

def initialize_connection():
    global socket_id, client_socket
    client_socket.connect((app_config.ip, app_config.port))

    handshake_data = client_socket.recv(1024).decode()
    handshake = json.loads(handshake_data)
    socket_id = handshake['socket_id']

    recv()

def close_connection():
    global client_socket, is_shutting_down

    if is_shutting_down:
        return
    is_shutting_down = True

    print("Closing connection...")
    try:
        client_socket.shutdown(socket.SHUT_RDWR)
    except Exception as e:
        print(f"Error closing socket: {e}")


def login(username, password: str):
    try:
        res = requests.post(f'http://{app_config.ip}:{app_config.http_port}/users/login',
                                data={"username": username, "password": password, "socket_id": socket_id})
        user_id = res.json()['user_id']
        return {"status": "success", "user_id": user_id, "username": username, "message": "Login successful"}
    except Exception as e:
        print(f"Login Error: {e}")
        return {"status": "error", "message": "Invalid credentials or server error"}

def register(username, password):
    try:
        res = requests.post(f'http://{app_config.ip}:{app_config.http_port}/users/register',
                                data={"username": username, "password": password, "socket_id": socket_id})
        user_id = res.json()['user_id']
        return {"status": "success", "user_id": user_id, "username": username, "message": "Account created"}
    except Exception as e:
        print(f"Register Error: {e}")
        return {"status": "error", "message": "Could not register"}

def send(message:str, sender_id: str,conversation_id: str):
    message_data = {
        "sender_id": sender_id,
        "conversation_id": conversation_id,
        "content": message,
        "created_at": datetime.now().isoformat()
    }
    client_socket.send(json.dumps(message_data).encode())

def recv():
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("Disconnected from server")
                client_socket.close()
                break
            
            try:
                # Debug print raw data
                message = Message.from_json(data.decode())

                cid = str(message.conversation_id)
                text = message.content
                sender_id = str(message.sender_id)
                # Format stamp like '5:30pm'
                stamp = message.created_at.strftime('%I:%M%p').lstrip('0').lower()

                # Update state
                chat_messages.setdefault(cid, []).append({
                    'text': text,
                    'sent': sender_id == current_user_id['value'],
                    'stamp': stamp,
                    'status': 'pending'
                })

                # Check if we know this conversation
                known_ids = {str(c['id']) for c in CHATS}
                if cid not in known_ids:
                    # Fetch conversation details
                    conv = api.get_conversation(cid, current_user_id['value'])
                    if conv:
                        # Parse it to UI format
                        parsed_conv = {
                            'id': conv['id'],
                            'name': conv['members'][0]['username'] if conv['type'] == 0 else conv['name'],
                            'members': len(conv['members']) if conv['type'] == 0 else len(conv['members']) + 1,
                            'start_date': conv['created_at'],
                            'type': conv['type'],
                        }
                        CHATS.append(parsed_conv)
                        # Refresh sidebar
                        if main_loop:
                            def _refresh_sidebar():
                                # We need sidebar_refs to be accessible
                                from client.ui.chat import sidebar_refs
                                if sidebar_refs:
                                    # Need to re-filter chats because sidebar uses filtered_chats() which reads from CHATS
                                    # But filtered_chats() reads the global CHATS list directly.
                                    render_chat_lists(chat_list_containers=sidebar_refs.chat_list_containers, on_select_chat=select_chat_action)
                                else:
                                    print("Sidebar refs not found")
                            
                            main_loop.call_soon_threadsafe(_refresh_sidebar)
                    else:
                        print("Failed to fetch conversation details")

                # Update UI if relevant
                if cid == selected_chat['id'] and main_loop:
                    def _update():
                        render_messages()

                    main_loop.call_soon_threadsafe(_update)
            except Exception as e:
                print(f"Error processing message: {e}")

        except Exception as e:
            print(f"Error receiving data: {e}")
            client_socket.close()
            break
    
    app.shutdown()
    os._exit(0)


def main():
    initialize_ui(on_login=login, on_register=register, on_send=send)
    
    app.on_disconnect(close_connection)

    ui.timer(0, connect_worker, once=True)