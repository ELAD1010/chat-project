import socket
import threading
import json
from dotenv import load_dotenv
from uuid import UUID, uuid4
from chat.auxiliary.message import Message
from config.app_config import AppConfig


def send(cli_sock):
    dest_client_id = input("Enter client ID\r\n")
    text = input("Enter your message\r\n")
    dest_client_uuid = UUID(dest_client_id)
    message = Message(sender_id=uuid4(), receiver_id=dest_client_uuid, content=text)
    data = json.dumps(message, default=lambda obj: obj.__dict__())
    cli_sock.send(data.encode())


def main():
    load_dotenv()
    app_config = AppConfig()
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli_sock.connect((app_config.ip, app_config.port))
    threading.Thread(target=send, args=(cli_sock,), daemon=True).start()
    while True:
        data = cli_sock.recv(1024).decode()
        message = Message.from_json(data)
        print(message)


if __name__ == '__main__':
    main()