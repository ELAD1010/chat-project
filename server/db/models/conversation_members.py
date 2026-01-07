import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, CHAR, Uuid
from sqlalchemy.orm import relationship, Mapped
from server.db.db_manager import Base


class ConversationMembers(Base):
    __tablename__ = 'conversation_members'
    conversation_id: Mapped[uuid.UUID] = Column(ForeignKey("conversations.id"), primary_key=True)
    user_id: Mapped[uuid.UUID] = Column(ForeignKey("users.id"), primary_key=True)
    joined_at = Column(DateTime(timezone=True), default=datetime.now)
    conversation: Mapped["Conversation"] = relationship(back_populates="members")
    user:  Mapped["User"] = relationship(back_populates="conversations")