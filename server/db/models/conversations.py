import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, String, Enum, Uuid
from sqlalchemy.orm import relationship, Mapped
from server.db.db_manager import Base
from server.enums.conversation_enums import ConversationType


class Conversation(Base):
    __tablename__ = 'conversations'
    id: Mapped[uuid.UUID] = Column(Uuid, primary_key=True, default=uuid.uuid4)
    type = Column(Enum(ConversationType))
    name = Column(String(80),  nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    members: Mapped[list["ConversationMembers"]] = relationship(back_populates="conversation",
    )
