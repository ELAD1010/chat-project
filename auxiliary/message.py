import json
import datetime
from datetime import datetime
from dataclasses import dataclass, field
from uuid import UUID, uuid4

@dataclass
class Message:
    sender_id: UUID
    receiver_id: UUID
    content: str
    id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.now)

    @classmethod
    def from_json(cls, json_str):
        message_dict = json.loads(json_str)

        # Manual conversion happens here
        return cls(
            id=UUID(message_dict['id']),
            sender_id=UUID(message_dict['sender_id']),
            receiver_id=UUID(message_dict['receiver_id']),
            timestamp=datetime.fromisoformat(message_dict['timestamp']),
            content=message_dict['content']
        )

    def __dict__(self):
        return {"id": str(self.id), "sender_id": str(self.sender_id), "receiver_id": str(self.receiver_id), "content": self.content, "timestamp": str(self.timestamp)}
