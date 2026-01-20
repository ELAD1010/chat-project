from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from nicegui import ui

from client.ui.app_state import chat_by_id, chat_messages, now_stamp, selected_chat, current_user_id, current_username
from client.ui.messages_view import MessagesRefs, build_messages_list_container, render_messages
from client.ui.sidebar import SidebarRefs, render_chat_lists
from client.ui.welcome_ui import build_welcome_view


@dataclass
class ChatLayoutRefs:
    welcome_view: ui.element
    chat_view: ui.element
    chat_title: ui.label
    chat_avatar_initial: ui.label
    conversation_date_pill: ui.label
    sidebar_refs: SidebarRefs
    messages_refs: MessagesRefs
    on_select_chat: Callable[[str], None]


def build_chat_content(
    *,
    sidebar_refs: SidebarRefs,
    build_composer_row: Callable[[str], None],
    on_send_backend: Callable[[str, str, str], None],
) -> ChatLayoutRefs:
    """Build the right content pane: welcome (default) + chat view (hidden until selection)."""

    # Messages list container must be created inside the message scroll region.
    messages_refs: MessagesRefs | None = None

    def select_chat(chat_id: str) -> None:
        selected_chat['id'] = chat_id
        chat = chat_by_id(chat_id)
        try:
            welcome_view.classes(add='hidden')
            chat_view.classes(remove='hidden')
        except Exception:
            pass
        chat_title.set_text(chat['name'])
        chat_avatar_initial.set_text((chat['name'][:1] or '?').upper())
        conversation_date_pill.set_text(chat.get('start_date', ''))
        if messages_refs:
            render_messages(messages_refs, scroll_to_bottom=True)
        render_chat_lists(chat_list_containers=sidebar_refs.chat_list_containers, on_select_chat=select_chat)

    welcome_view, subtitle_label = build_welcome_view(
        title='Welcome',
        subtitle='We missed you!',
    )
    subtitle_label.bind_text_from(current_username, 'value', backward=lambda u: f'We missed you, {u}!')

    chat_view = ui.element('div').classes('w-full h-full min-h-0 overflow-hidden hidden flex flex-col')
    with chat_view:
        with ui.row().classes('w-full py-2.5 bg-[#272727] shrink-0'):
            with ui.row().classes('w-full items-center gap-3 px-6'):
                with ui.element('div').classes('w-10 h-10 rounded-full bg-white/10 border border-white/10 flex items-center justify-center'):
                    chat_avatar_initial = ui.label((chat_by_id(selected_chat['id'])['name'][:1] or '?').upper()).classes('text-white font-semibold')
                chat_title = ui.label(chat_by_id(selected_chat['id'])['name']).classes('text-white text-lg font-semibold')

        with ui.element('div').classes('flex-1 min-h-0 h-0 w-full max-w-4xl mx-auto px-5 pt-3 pb-6 message_scroll overflow-y-auto').props('id=message-scroll'):
            conversation_date_pill = ui.label('') \
                .classes('self-center mb-4 px-4 py-1 rounded-full bg-white/10 text-gray-200 text-sm')

            messages_refs = build_messages_list_container()

        with ui.row().classes('w-full justify-center px-5 pb-6 shrink-0'):
            def _on_send(text: str) -> None:
                if not selected_chat.get('id'):
                    return
                chat_messages.setdefault(selected_chat['id'], []).append(
                    {'text': text, 'sent': True, 'stamp': now_stamp(), 'status': 'pending'}
                )
                if messages_refs:
                    render_messages(messages_refs, scroll_to_bottom=True)

                if current_user_id['value']:
                    on_send_backend(text, current_user_id['value'], selected_chat['id'])
                else:
                    print("Error: No user ID found in state.")

            build_composer_row(_on_send)

    # initial render keeps welcome visible; chat hidden
    return ChatLayoutRefs(
        welcome_view=welcome_view,
        chat_view=chat_view,
        chat_title=chat_title,
        chat_avatar_initial=chat_avatar_initial,
        conversation_date_pill=conversation_date_pill,
        sidebar_refs=sidebar_refs,
        messages_refs=messages_refs,
        on_select_chat=select_chat,
    )


