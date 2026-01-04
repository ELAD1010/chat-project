from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from nicegui import ui

from app_state import filtered_chats, initial, selected_chat


@dataclass
class SidebarRefs:
    chat_list_containers: list[ui.element]


def build_sidebar(*, on_select_chat: Callable[[str], None]) -> SidebarRefs:
    """Build the left sidebar. Chat list rendering is handled via render_chat_lists()."""
    chat_list_containers: list[ui.element] = []

    def on_chat_search(e) -> None:
        # late import to avoid circular import; state is shared via module globals
        from app_state import chat_search

        chat_search['value'] = e.value or ''
        render_chat_lists(chat_list_containers=chat_list_containers, on_select_chat=on_select_chat)

    # flex/min-h-0 are critical so the chat list can become a bounded scroll region
    with ui.column().classes('h-full min-h-0 w-full flex flex-col'):
        ui.label('Chats').classes('text-white text-3xl font-semibold tracking-tight')
        with ui.row().classes('mt-5 w-full items-center bg-white/5 border border-white/10 rounded-2xl px-4 '):
            search_input = ui.input(placeholder='Search chats') \
                .props('borderless dense input-class="text-gray-200 placeholder-gray-400 text-base"') \
                .classes('grow text-base')
            ui.icon('search').classes('text-gray-300 text-lg')
            search_input.on_value_change(on_chat_search)

        # Full-width scroll container (avoid negative margins which can make items look "inset")
        chat_list = ui.element('div').classes('sidebar_scroll mt-4 flex-1 min-h-0 w-full overflow-y-auto')
        chat_list_containers.append(chat_list)
        render_chat_lists(chat_list_containers=chat_list_containers, on_select_chat=on_select_chat)

    return SidebarRefs(chat_list_containers=chat_list_containers)


def render_chat_lists(*, chat_list_containers: list[ui.element], on_select_chat: Callable[[str], None]) -> None:
    for container in chat_list_containers:
        container.clear()
        with container:
            for c in filtered_chats():
                is_active = (c['id'] == selected_chat['id'])
                row_cls = (
                    'w-full flex flex-row items-center gap-3 py-3 px-3 rounded-xl cursor-pointer transition-colors '
                    + ('bg-white/10' if is_active else 'hover:bg-white/5')
                )
                with ui.row().classes(row_cls).style('width: 100%;').on('click', lambda e, cid=c['id']: on_select_chat(cid)):
                    # Avatar
                    with ui.element('div').classes('w-10 h-10 rounded-full bg-white/10 border border-white/10 flex items-center justify-center'):
                        if c.get('members') == 2:
                            # Contact chat: profile image if available, otherwise fallback to initial
                            if c.get('avatar_url'):
                                ui.image(c['avatar_url']).classes('w-full h-full rounded-full object-cover')
                            else:
                                ui.label(initial(c.get('name', ''))).classes('text-white font-semibold')
                        else:
                            # Group chat: generic icon
                            ui.icon('group').classes('text-gray-200')
                    with ui.column().classes('gap-0'):
                        ui.label(c['name']).classes('text-gray-100 font-medium leading-tight text-base')
                        ui.label(f"{c['members']} members").classes('text-gray-400 text-sm leading-tight')


