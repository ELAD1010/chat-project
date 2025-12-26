import threading
import socket
import json
from queue import Queue
from auxiliary.message import Message
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

    def cleanup_connection(self):
        self.cli_sock.shutdown(socket.SHUT_RDWR)
        self.cli_sock.close()
        for client_id in self.clients_dict:
            if self.clients_dict == self.clients_dict[client_id]:
                del self.clients_dict[client_id]

        self.out_queue.put(None)  # Send signal to the send thread to be killed

    def receive(self):
        while True:
            try:
                data = self.cli_sock.recv(BUFFER_SIZE)
                if not data:
                    print("Client disconnected cleanly")
                    self.cleanup_connection()
                    break

                message = Message.from_json(data.decode())
                dest_client = self.clients_dict[message.receiver_id]
                dest_client.out_queue.put(message)

            except ConnectionResetError:
                # Handle abrupt os disconnection error
                print("Client connection was forcibly closed")
                self.cleanup_connection()
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                self.cleanup_connection()
                break

    def send(self):
        while True:
            message: Message = self.out_queue.get()
            if message is None:
                break
            data = json.dumps(message, default=lambda obj: obj.__dict__())
            self.cli_sock.send(data.encode())

