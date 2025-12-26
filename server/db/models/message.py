import uuid
from datetime import datetime
from sqlalchemy import ForeignKey, Column, CHAR, DateTime, String, Uuid
from sqlalchemy.orm import Mapped

from server.db.db_manager import Base


class Message(Base):
    __tablename__ = 'messages'
    id = Column(CHAR(50), primary_key=True, default=uuid.uuid4)
    sender_id: Mapped[uuid.UUID] = Column(Uuid, ForeignKey("users.id"))
    receiver_id:  Mapped[uuid.UUID] = Column(Uuid, ForeignKey("users.id"))
    content = Column(String(255))
    timestamp = Column(DateTime(timezone=True), default=datetime.now)