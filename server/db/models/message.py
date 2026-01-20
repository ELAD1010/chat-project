import uuid
from datetime import datetime
from sqlalchemy import ForeignKey, Column, CHAR, DateTime, String, Uuid
from sqlalchemy.orm import Mapped

from server.db.db_manager import Base


class Message(Base):
    __tablename__ = 'messages'
    id: Mapped[uuid.UUID] = Column(Uuid, primary_key=True, default=uuid.uuid4)
    conversation_id: Mapped[uuid.UUID] = Column(Uuid, ForeignKey("conversations.id"))
    sender_id: Mapped[uuid.UUID] = Column(Uuid, ForeignKey("users.id"))
    content = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=datetime.now)