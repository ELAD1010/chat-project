from __future__ import annotations

from datetime import datetime

# --- Static chat list (dummy data for UI) ---
CHATS = [
    {'id': 'jack', 'name': 'Jack', 'members': 2, 'start_date': 'March 3'},
    {'id': 'dana', 'name': 'Dana', 'members': 2, 'start_date': 'March 12'},
    {'id': 'yuli', 'name': 'Yuli', 'members': 2, 'start_date': 'April 1'},
    {'id': 'dan', 'name': 'Dan', 'members': 2, 'start_date': 'April 18'},
    {'id': 'ron', 'name': 'Ron', 'members': 2, 'start_date': 'May 6'},
    {'id': 'moshe', 'name': 'Moshe', 'members': 2, 'start_date': 'May 27'},
    {'id': 'noa', 'name': 'Noa', 'members': 2, 'start_date': 'June 9'},
    {'id': 'lori', 'name': 'Lori', 'members': 2, 'start_date': 'July 2'},
    {'id': 'maya', 'name': 'Maya', 'members': 2, 'start_date': 'July 18'},
    {'id': 'liam', 'name': 'Liam', 'members': 3, 'start_date': 'August 4'},
    {'id': 'aria', 'name': 'Aria', 'members': 2, 'start_date': 'August 22'},
    {'id': 'noam', 'name': 'Noam', 'members': 2, 'start_date': 'September 1'},
    {'id': 'talia', 'name': 'Talia', 'members': 4, 'start_date': 'September 10'},
    {'id': 'eden', 'name': 'Eden', 'members': 2, 'start_date': 'September 26'},
    {'id': 'amir', 'name': 'Amir', 'members': 3, 'start_date': 'October 3'},
    {'id': 'shai', 'name': 'Shai', 'members': 2, 'start_date': 'October 11'},
    {'id': 'yael', 'name': 'Yael', 'members': 2, 'start_date': 'October 24'},
    {'id': 'levi', 'name': 'Levi', 'members': 5, 'start_date': 'November 2'},
    {'id': 'nina', 'name': 'Nina', 'members': 2, 'start_date': 'November 9'},
    {'id': 'omer', 'name': 'Omer', 'members': 3, 'start_date': 'November 18'},
    {'id': 'sara', 'name': 'Sara', 'members': 2, 'start_date': 'November 29'},
    {'id': 'ben', 'name': 'Ben', 'members': 2, 'start_date': 'December 6'},
    {'id': 'ella', 'name': 'Ella', 'members': 4, 'start_date': 'December 12'},
    {'id': 'itai', 'name': 'Itai', 'members': 2, 'start_date': 'December 18'},
    {'id': 'ruth', 'name': 'Ruth', 'members': 3, 'start_date': 'December 21'},
    {'id': 'david', 'name': 'David', 'members': 2, 'start_date': 'December 24'},
    {'id': 'noga', 'name': 'Noga', 'members': 2, 'start_date': 'January 4'},
    {'id': 'gal', 'name': 'Gal', 'members': 3, 'start_date': 'January 12'},
    {'id': 'matan', 'name': 'Matan', 'members': 2, 'start_date': 'January 20'},
    {'id': 'adi', 'name': 'Adi', 'members': 2, 'start_date': 'February 1'},
    {'id': 'yonatan', 'name': 'Yonatan', 'members': 4, 'start_date': 'February 9'},
    {'id': 'lea', 'name': 'Lea', 'members': 2, 'start_date': 'February 16'},
    {'id': 'hila', 'name': 'Hila', 'members': 3, 'start_date': 'February 23'},
    {'id': 'gil', 'name': 'Gil', 'members': 2, 'start_date': 'March 1'},
]

# --- UI state (kept as dicts to preserve existing semantics) ---
# No chat selected by default: show welcome screen until the user clicks a chat.
selected_chat = {'id': None}
chat_search = {'value': ''}
chat_messages: dict[str, list[dict]] = {}

# Seed a few dummy messages so the UI looks alive
for c in CHATS:
    chat_messages[c['id']] = [
        {'text': f'Hey {c["name"]}, how are you?', 'sent': False, 'stamp': '12:19pm'},
        {'text': "I'm doing great!", 'sent': True, 'stamp': '12:20pm', 'status': 'pending'},
    ]


def now_stamp() -> str:
    return datetime.now().strftime('%I:%M%p').lstrip('0').lower()


def chat_by_id(chat_id: str | None) -> dict:
    if not chat_id:
        return CHATS[0]
    return next((c for c in CHATS if c['id'] == chat_id), CHATS[0])


def filtered_chats() -> list[dict]:
    q = (chat_search['value'] or '').strip().lower()
    if not q:
        return CHATS
    return [c for c in CHATS if q in c['name'].lower()]


def initial(name: str) -> str:
    return ((name or '?')[:1]).upper()


