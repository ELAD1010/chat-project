from __future__ import annotations

from dataclasses import dataclass

from nicegui import ui

from client.ui.app_state import chat_messages, selected_chat


@dataclass
class MessagesRefs:
    messages_list: ui.element


def build_messages_list_container() -> MessagesRefs:
    messages_list = ui.column().classes('w-full gap-1')
    return MessagesRefs(messages_list=messages_list)


def render_messages(refs: MessagesRefs, *, scroll_to_bottom: bool = True) -> None:
    """Render the current chat messages into the messages list container.

    During app startup there is no active NiceGUI event loop/client yet, so any JS execution
    must be guarded.
    """
    refs.messages_list.clear()
    current = chat_messages.get(selected_chat['id'], [])

    def _stamp_with_status(m: dict) -> str:
        stamp = (m.get('stamp', '') or '').strip()
        status = m.get('status')
        # For now we only support "pending" (clock). Future: sent/received/seen.
        if status == 'pending':
            return f'{stamp}  🕒'.strip()
        return stamp

    with refs.messages_list:
        for m in current:
            if m.get('sent'):
                with ui.column().classes('w-full place-items-end'):
                    ui.chat_message(
                        text=m.get('text', ''),
                        sent=True,
                        stamp=_stamp_with_status(m),
                    ).props('bg-color="green-2" text-color="black" size="md"') \
                        .classes('text-sm md:text-base lg:text-lg')
            else:
                with ui.column().classes('w-full place-items-start'):
                    ui.chat_message(
                        text=m.get('text', ''),
                        sent=False,
                        stamp=_stamp_with_status(m),
                    ).props('bg-color="white" text-color="black" size="md"') \
                        .classes('text-sm md:text-base lg:text-lg')
    if scroll_to_bottom:
        try:
            with refs.messages_list:
                ui.run_javascript("""
                    const el = document.getElementById('message-scroll');
                    if (el) { el.scrollTop = el.scrollHeight; }
                """)
        except (AssertionError, RuntimeError):
            pass


