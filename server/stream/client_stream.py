import threading
import socket
import json
from queue import Queue
from chat.auxiliary.message import Message
from uuid import UUID

BUFFER_SIZE = 1024


class ClientStream:
    def __init__(self, address, cli_sock, clients_dict: dict[UUID, "ClientStream"]):
        self.ip = address[0]
        self.port = address[1]
        self.cli_sock: socket.socket = cli_sock
        self.clients_dict = clients_dict
        self.out_queue = Queue()

        # Daemon threads so Ctrl+C can terminate the process immediately.
        threading.Thread(target=self.receive, daemon=True).start()
        threading.Thread(target=self.send, daemon=True).start()

    def receive(self):
        data = self.cli_sock.recv(BUFFER_SIZE).decode()
        message = Message.from_json(data)
        dest_client = self.clients_dict[message.receiver_id]
        dest_client.out_queue.put(message)
        print(data)

    def send(self):
        message: Message = self.out_queue.get()
        data = json.dumps(message, default=lambda obj: obj.__dict__())
        self.cli_sock.send(data.encode())

