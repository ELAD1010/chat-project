import threading
import uuid
from collections import defaultdict

from server.decorators.singleton import singleton


@singleton
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[uuid.UUID, "ClientStream"] = {}
        self.rooms = defaultdict(set)
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
                stream.set_user_id(real_user_id)
                # 2. Re-save it under the user's permanent ID
                self.active_connections[real_user_id] = stream
                return True
            return False

    def join_room(self, user_id, conversation_id):
        with self._lock:
            if user_id not in self.active_connections:
                return
            self.rooms[conversation_id].add(user_id)
            print(f"User {user_id} joined room {conversation_id}")

    def bulk_join_rooms(self, user_id, conversation_ids: list):
        """Adds a user to MANY conversation rooms at once"""
        with self._lock:
            if user_id not in self.active_connections:
                return
            for conversation_id in conversation_ids:
                self.rooms[conversation_id].add(user_id)

    def leave_room(self, user_id, conversation_id):
        with self._lock:
            if conversation_id in self.rooms:
                self.rooms[conversation_id].discard(user_id)

    def get_room_members(self, conversation_id):
        """Returns a list of client streams in this room"""
        streams = []
        with self._lock:
            # Get all user IDs in the room
            user_ids = self.rooms.get(conversation_id, set())

            # Find their active streams
            for uid in user_ids:
                if uid in self.active_connections:
                    streams.append(self.active_connections[uid])
        return streams