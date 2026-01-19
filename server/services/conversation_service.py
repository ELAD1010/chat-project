import uuid
from sqlalchemy.orm import joinedload, selectinload
from server.enums.conversation_enums import ConversationType
from server.db.db_manager import DBManager
from server.db.models import Conversation, User, ConversationMembers
from server.utils import model_to_dict

class ConversationService:
    def __init__(self):
        self.db: DBManager = DBManager()

    def get_conversations_by_user_id(self, user_id):
        with self.db as session:
            conversations = session.query(ConversationMembers)\
                .options(
                joinedload(ConversationMembers.user),
                joinedload(ConversationMembers.conversation)
                .selectinload(Conversation.members)  # Load the list of members
                .joinedload(ConversationMembers.user))\
                .filter((ConversationMembers.user_id == user_id)).all()

            results = []
            for conversation in conversations:
                # Convert the main member object to a dict
                conversation_dict = model_to_dict(conversation)

                # Manually Convert and Add the related Conversation object
                if conversation.conversation:
                    conversation_dict = {**conversation_dict, **model_to_dict(conversation.conversation)}
                    del conversation_dict['conversation_id']  # Remove redundant field
                    members = []
                    for member in conversation.conversation.members:
                        if user_id == member.user_id:
                            continue  # Skip adding the requesting user to the members list
                        member_dict = model_to_dict(member.user)
                        members.append({"user_id": member_dict['id'], "username": member_dict['username']})
                    conversation_dict['members'] = members

                results.append(conversation_dict)

            return results

    def get_conversation_by_id(self, conversation_id: str, user_id: str = None):
        with self.db as session:
            conversation = session.query(Conversation) \
                .options(selectinload(Conversation.members).joinedload(ConversationMembers.user)) \
                .filter(Conversation.id == uuid.UUID(conversation_id)) \
                .first()

            if not conversation:
                return None

            conversation_dict = model_to_dict(conversation)
            members = []
            for member in conversation.members:
                if user_id and uuid.UUID(user_id) == member.user_id:
                    continue
                member_dict = model_to_dict(member.user)
                members.append({"user_id": member_dict['id'], "username": member_dict['username']})
            
            conversation_dict['members'] = members
            return conversation_dict

    def create_conversation(self, conversation_type: ConversationType, members: list[str], conversation_name: str = None):
        with self.db as session:
            conversation = Conversation(name=conversation_name, type=conversation_type)
            session.add(conversation)
            session.flush()

            for member_id in members:
                conversation_member = ConversationMembers(user_id=uuid.UUID(member_id), conversation_id=conversation.id)
                session.add(conversation_member)

            session.commit()

            full_conversation = session.query(Conversation) \
                .options(
                selectinload(Conversation.members)
            ) \
                .filter(Conversation.id == conversation.id) \
                .one()

            result = model_to_dict(full_conversation)
            members = []
            for member in full_conversation.members:
                member_dict = model_to_dict(member.user)
                members.append({"user_id": member_dict['id'], "username": member_dict['username']})

            result['members'] = members
            return result

