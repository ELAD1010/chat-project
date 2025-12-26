from server.db.db_manager import DBManager
from server.db.models import Message
from auxiliary import message


class MessageService:
    def __init__(self):
        self.db: DBManager = DBManager()

    def get_messages_by_client_id(self, sender_id, receiver_id):
        with self.db as session:
            return session.query(Message)\
                .filter((Message.sender_id == sender_id & Message.receiver_id == receiver_id)
                        | (Message.sender_id == receiver_id & Message.receiver_id == sender_id)).all()

    def create_message(self, message: message.Message):
        db_message = Message(content=message.content, sender_id=message.sender_id, receiver_id=message.receiver_id)
        with self.db as session:
            session.add(db_message)