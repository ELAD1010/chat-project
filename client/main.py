import os
import socket
import threading
import json
import requests
from dotenv import load_dotenv
from auxiliary.message import Message
from client.config.app_config import AppConfig
from datetime import datetime

load_dotenv()

socket_id = None
app_config = AppConfig()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def initialize_connection():
    client_socket.connect((app_config.ip, app_config.port))

    handshake_data = client_socket.recv(1024).decode()
    handshake = json.loads(handshake_data)
    socket_id = handshake['socket_id']
    return socket_id

def login(username, password: str):
    res = requests.post(f'http://{app_config.ip}:{app_config.http_port}/users/login',
                              data={"username": username, "password": password, "socket_id": socket_id})
    client_id = res.json()['user_id']
    return client_id

def register(username, password):
    res = requests.post(f'http://{app_config.ip}:{app_config.http_port}/users/register',
                              data={"username": username, "password": password, "socket_id": socket_id})
    client_id = res.json()['user_id']
    return client_id

def send(message:str, sender_id: str,conversation_id: str):
    message_data = {
        "sender_id": sender_id,
        "conversation_id": conversation_id,
        "content": message,
        "timestamp": datetime.now().isoformat()
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

            message = Message.from_json(data.decode())
            print(message)
        except Exception as e:
            print(f"Error receiving data: {e}")
            client_socket.close()
            break

    os._exit(0)


def main():
    global socket_id
    # Needs to be executed first
    socket_id = initialize_connection()


if __name__ == '__main__':
    main()