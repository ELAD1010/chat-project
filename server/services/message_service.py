from server.db.db_manager import DBManager
from server.db.models import Message
from auxiliary import message
from server.utils import model_to_dict

class MessageService:
    def __init__(self):
        self.db: DBManager = DBManager()

    def get_messages_by_conversation_id(self, conversation_id):
        with self.db as session:
            messages = session.query(Message)\
                .filter((Message.conversation_id == conversation_id)).all()

            messages_arr = [model_to_dict(m) for m in messages]
            return messages_arr

    def create_message(self, message: message.Message):
        with self.db as session:
            db_message = Message(content=message.content, sender_id=message.sender_id,
                                 conversation_id=message.conversation_id, created_at=message.created_at)
            session.add(db_message)
            session.flush()
            return model_to_dict(db_message)
