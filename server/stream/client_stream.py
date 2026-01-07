import threading
import socket
import json
from queue import Queue
from auxiliary.message import Message
from server.connection_manager import ConnectionManager

BUFFER_SIZE = 1024


class ClientStream:
    def __init__(self, address, cli_sock, connection_manager: ConnectionManager):
        self.ip = address[0]
        self.port = address[1]
        self.cli_sock: socket.socket = cli_sock
        self.connection_manager = connection_manager
        self.user_id = None
        self.out_queue = Queue()

        # Daemon threads so Ctrl+C can terminate the process immediately.
        threading.Thread(target=self.receive, daemon=True).start()
        threading.Thread(target=self.send, daemon=True).start()

    def set_user_id(self, user_id):
        self.user_id = user_id

    def cleanup_connection(self):
        self.cli_sock.shutdown(socket.SHUT_RDWR)
        self.cli_sock.close()

        if self.user_id:
            self.connection_manager.remove_client(self.user_id)

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

                target_streams = self.connection_manager.get_room_members(message.conversation_id)

                for stream in target_streams:
                    if stream.user_id != self.user_id:
                        stream.out_queue.put(message)

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

