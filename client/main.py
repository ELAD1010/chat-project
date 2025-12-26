import os
import socket
import threading
import json
import requests
from dotenv import load_dotenv
from uuid import UUID
from auxiliary.message import Message
from client.config.app_config import AppConfig


def login(socket_id):
    username = input("Enter your username")
    res = requests.post('http://127.0.0.1:5000/users/login',
                              data={"username": username, "password": "1234", "socket_id": socket_id})
    client_id = res.json()['user_id']
    print(client_id)
    return client_id


def register(socket_id):
    username = input("Enter your username")
    res = requests.post('http://127.0.0.1:5000/users/register',
                              data={"username": username, "password": "1234", "socket_id": socket_id})
    client_id = res.json()['user_id']
    print(client_id)
    return client_id


def recv(cli_sock):
    while True:
        try:
            data = cli_sock.recv(1024)
            if not data:
                print("Disconnected from server")
                cli_sock.close()
                break

            message = Message.from_json(data.decode())
            print(message)
        except Exception as e:
            print(f"Error receiving data: {e}")
            cli_sock.close()
            break

    os._exit(0)


def main():
    load_dotenv()
    app_config = AppConfig()
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli_sock.connect((app_config.ip, app_config.port))

    handshake_data = cli_sock.recv(1024).decode()
    handshake = json.loads(handshake_data)
    socket_id = handshake['socket_id']

    action = input("login/register(L/R)")
    if action == 'L':
        user_id = login(socket_id)
    elif action == 'R':
        user_id = register(socket_id)
    else:
        cli_sock.close()
        return

    threading.Thread(target=recv, args=(cli_sock,), daemon=True).start()

    while True:
        dest_client_id = input("Enter client ID\r\n")
        text = input("Enter your message\r\n")
        dest_client_uuid = UUID(dest_client_id)
        message = Message(sender_id=user_id, receiver_id=dest_client_uuid, content=text)
        data = json.dumps(message, default=lambda obj: obj.__dict__())
        cli_sock.send(data.encode())


if __name__ == '__main__':
    main()