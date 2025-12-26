import threading
from server.decorators.singleton import singleton


@singleton
class ConnectionManager:
    def __init__(self):
        self.active_connections = {}
        self._lock = threading.Lock()

    def add_client(self, client_id, client_stream):
        with self._lock:
            self.active_connections[client_id] = client_stream

    def get_client(self, client_id):
        with self._lock:
            return self.active_connections.get(client_id)

    def remove_client(self, client_id):
        with self._lock:
            if client_id in self.active_connections:
                del self.active_connections[client_id]

    def promote_connection(self, temp_socket_id, real_user_id):
        """
        Swaps the key from the temporary UUID to the real User Database ID
        """
        with self._lock:
            if temp_socket_id in self.active_connections:
                # 1. Get the stream
                stream = self.active_connections.pop(temp_socket_id)
                # 2. Re-save it under the user's permanent ID
                self.active_connections[real_user_id] = stream
                return True
            return False