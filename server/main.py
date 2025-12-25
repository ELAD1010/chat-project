from uuid import uuid4
import socket
from queue import Queue
from dotenv import load_dotenv
from config.app_config import AppConfig
from stream.client_stream import ClientStream

def main():
    connected_clients = {}
    load_dotenv()
    app_config = AppConfig()

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((app_config.ip, app_config.port))
    server_sock.listen(8)

    while True:
        cli_sock, address = server_sock.accept()
        client_id = uuid4()
        print(client_id)
        client_stream = ClientStream(address, cli_sock, connected_clients)
        connected_clients[client_id] = client_stream



if __name__ == '__main__':
    main()