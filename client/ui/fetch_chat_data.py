from __future__ import annotations

from datetime import datetime


def fetch_chats_list(user_id: str) -> list[dict]:
    """Dummy fetch for chats list.

    Returns the UI-ready chat shape used across the app:
    {id, name, members, start_date, avatar_url?}
    """
    _ = user_id  # unused in dummy implementation
    return [
        {'id': 'jack', 'name': 'Jack', 'members': 2, 'start_date': 'March 3'},
        {'id': 'dana', 'name': 'Dana', 'members': 2, 'start_date': 'March 12'},
        {'id': 'group-1', 'name': 'Rift Team', 'members': 5, 'start_date': 'April 7'},
    ]


def fetch_chat_messages(chat_id: str) -> list[dict]:
    """Dummy fetch for chat messages.

    Returns the UI-ready message shape:
    {text, sent, stamp, status?}
    """
    now = datetime.now().strftime('%I:%M%p').lstrip('0').lower()
    if chat_id == 'group-1':
        return [
            {'text': 'Welcome to the team chat!', 'sent': False, 'stamp': '9:03am'},
            {'text': 'Glad to be here.', 'sent': True, 'stamp': '9:04am', 'status': 'pending'},
        ]
    return [
        {'text': f'Hey {chat_id}, how are you?', 'sent': False, 'stamp': now},
        {'text': "I'm doing great!", 'sent': True, 'stamp': now, 'status': 'pending'},
    ]