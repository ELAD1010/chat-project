from __future__ import annotations

import requests
import json
from datetime import datetime
from client.ui.app_state import current_user_id

from client import api 


def fetch_chats_list(user_id: str) -> list[dict]:

    conversations = api.get_user_conversations(user_id)

    parsed_conversations = []
    for conversation in conversations:
        parsed_conversations.append({
            'id': conversation['id'],
            'name': conversation['members'][0]['username'] if conversation['type'] == 0 else conversation['name'],
            'members': len(conversation['members']) if conversation['type'] == 0 else len(conversation['members']) + 1,
            'start_date': conversation['created_at'],
            'type': conversation['type'],
        })

    return parsed_conversations


def fetch_chat_messages(chat_id: str) -> list[dict]:

    messages = api.get_conversation_messages(chat_id)

    print(current_user_id['value'])
    parsed_messages = []
    for message in messages:
        parsed_messages.append({
            'text': message['content'],
            'sent': message['sender_id'] == current_user_id['value'],
            'stamp': message['created_at'],
            'status': 'pending' if not message.get('delivered_at') else 'sent'
        })
    
    return parsed_messages
    