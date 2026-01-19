from __future__ import annotations

from datetime import datetime

# --- Chats & messages data (populated on auth success via fetch_chat_data) ---
CHATS: list[dict] = []

# --- UI state (kept as dicts to preserve existing semantics) ---
# No chat selected by default: show welcome screen until the user clicks a chat.
selected_chat = {'id': None}
current_user_id = {'value': None}
current_username = {'value': ''}
chat_search = {'value': ''}
chat_messages: dict[str, list[dict]] = {}
loading_state = {'value': False}


def load_chat_data(user_id: str) -> None:
    """Load chats list + messages into app_state using fetch_chat_data dummy layer."""
    from client.ui.fetch_chat_data import fetch_chat_messages, fetch_chats_list

    chats = fetch_chats_list(user_id)
    CHATS.clear()
    CHATS.extend(chats)

    chat_messages.clear()
    for c in CHATS:
        cid = c.get('id')
        if not cid:
            continue
        chat_messages[cid] = fetch_chat_messages(str(cid))

    # Reset selection/search on load to preserve current UX
    selected_chat['id'] = None
    chat_search['value'] = ''
    loading_state['value'] = False


def now_stamp() -> str:
    return datetime.now().strftime('%I:%M%p').lstrip('0').lower()


def chat_by_id(chat_id: str | None) -> dict:
    # During startup (before auth/data fetch) CHATS can be empty; return a safe placeholder.
    if not CHATS:
        return {'id': '', 'name': '', 'members': 0, 'start_date': ''}
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


