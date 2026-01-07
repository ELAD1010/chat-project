from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime, Uuid
from sqlalchemy.orm import relationship, Mapped
from server.db.db_manager import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[uuid.UUID] = Column(Uuid, primary_key=True, default=uuid.uuid4)
    username = Column(String(80))
    password = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    conversations: Mapped[list["ConversationMembers"]] = relationship(
        back_populates="user",
    )
