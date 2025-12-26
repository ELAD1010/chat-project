import json
from uuid import uuid4
import socket
import threading
from dotenv import load_dotenv

from server.config.app_config import AppConfig
from server.stream.client_stream import ClientStream
from server.db.db_manager import DBManager
from server.http_server.http_server import run_http_server
from server.connection_manager import ConnectionManager


def main():
    load_dotenv()
    app_config: AppConfig = AppConfig()

    db = DBManager(app_config.db_name)
    db.create_tables()

    http_thread = threading.Thread(
        target=run_http_server,
        args=(app_config.ip, app_config.http_port),
        daemon=True  # Ensures this thread dies when the main program exits
    )

    http_thread.start()

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((app_config.ip, app_config.port))
    server_sock.listen(8)

    connection_manager: ConnectionManager = ConnectionManager()

    while True:
        cli_sock, address = server_sock.accept()

        temp_socket_id = uuid4()
        client_stream = ClientStream(address, cli_sock, connection_manager.active_connections)
        connection_manager.add_client(temp_socket_id, client_stream)
        init_msg = json.dumps({"type": "HANDSHAKE", "socket_id": str(temp_socket_id)})
        cli_sock.send(init_msg.encode())

        print(f"Client connected. Ticket: {temp_socket_id}")


if __name__ == '__main__':
    main()
