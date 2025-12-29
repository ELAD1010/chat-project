from datetime import datetime

from nicegui import app, ui
from category_svgs import CATEGORY_SVGS
from emoji_data import EMOJI_ALIASES, EMOJI_CATEGORIES

# --- SETUP BACKGROUND ---
app.add_static_files('/static', 'assets')
ui.query('body').style(
    'background-image: url("/static/wallpaper.svg");'
    'background-size: cover;'
    'background-position: center;'
    'background-attachment: fixed;'
    'background-color: #1a1a1a;'
    'margin: 0;'
    'padding: 0;'
    'overflow: hidden;'
)

def _now_stamp() -> str:
    return datetime.now().strftime('%I:%M%p').lstrip('0').lower()


ui.add_head_html(
    """
<style>
html, body, #q-app { height: 100%; }
html, body { padding: 0 !important; }
/* NiceGUI/Quasar root containers sometimes add padding/margins; force edge-to-edge layout */
#q-app, .q-layout, .q-page-container, .q-page {
  padding: 0 !important;
  margin: 0 !important;
}
/* NiceGUI outer content wrapper (defaults to 16px padding) */
.nicegui-content {
  padding: 0 !important;
}
.emoji_picker_card * { box-sizing: border-box; }
.emoji_cat_strip { display:flex; flex-wrap:nowrap; gap:6px; overflow-x:auto; padding: 2px 2px 0 2px; }
.emoji_cat_strip::-webkit-scrollbar { width:0; height:0; display:none; }
.emoji_grid { overflow-y:auto; scrollbar-width: thin; }
.emoji_btn { min-width: 36px; height: 36px; }
.sidebar_scroll { overflow-y: auto; }
.sidebar_scroll::-webkit-scrollbar { width: 0; height: 0; display: none; }
.sidebar_scroll { scrollbar-width: none; }
.message_scroll { overflow-y: auto; scrollbar-width: none; -ms-overflow-style: none; }
.message_scroll::-webkit-scrollbar { width: 0; height: 0; display: none; }
</style>
    """.strip()
)


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

selected_chat = {'id': CHATS[0]['id']}
chat_search = {'value': ''}
chat_messages: dict[str, list[dict]] = {}

for c in CHATS:
    # Seed a few dummy messages so the UI looks alive
    chat_messages[c['id']] = [
        {'text': f'Hey {c["name"]}, how are you?', 'sent': False, 'stamp': '12:19pm'},
        {'text': "I'm doing great!", 'sent': True, 'stamp': '12:20pm', 'status': 'pending'},
    ]

def _chat_by_id(chat_id: str) -> dict:
    return next((c for c in CHATS if c['id'] == chat_id), CHATS[0])

def _filtered_chats() -> list[dict]:
    q = (chat_search['value'] or '').strip().lower()
    if not q:
        return CHATS
    return [c for c in CHATS if q in c['name'].lower()]

def _initial(name: str) -> str:
    return ((name or '?')[:1]).upper()

chat_list_containers: list[ui.element] = []

def render_chat_lists() -> None:
    for container in chat_list_containers:
        container.clear()
        with container:
            for c in _filtered_chats():
                is_active = (c['id'] == selected_chat['id'])
                row_cls = (
                    'w-full flex flex-row items-center gap-3 py-3 px-3 rounded-xl cursor-pointer transition-colors '
                    + ('bg-white/10' if is_active else 'hover:bg-white/5')
                )
                with ui.row().classes(row_cls).style('width: 100%;').on('click', lambda e, cid=c['id']: select_chat(cid)):
                    # Avatar
                    with ui.element('div').classes('w-10 h-10 rounded-full bg-white/10 border border-white/10 flex items-center justify-center'):
                        if c.get('members') == 2:
                            # Contact chat: profile image if available, otherwise fallback to initial
                            if c.get('avatar_url'):
                                ui.image(c['avatar_url']).classes('w-full h-full rounded-full object-cover')
                            else:
                                ui.label(_initial(c.get('name', ''))).classes('text-white font-semibold')
                        else:
                            # Group chat: generic icon
                            ui.icon('group').classes('text-gray-200')
                    with ui.column().classes('gap-0'):
                        ui.label(c['name']).classes('text-gray-100 font-medium leading-tight text-base')
                        ui.label(f"{c['members']} members").classes('text-gray-400 text-sm leading-tight')

def select_chat(chat_id: str) -> None:
    selected_chat['id'] = chat_id
    chat = _chat_by_id(chat_id)
    chat_title.set_text(chat['name'])
    chat_avatar_initial.set_text((chat['name'][:1] or '?').upper())
    conversation_date_pill.set_text(chat.get('start_date', ''))
    render_messages(scroll_to_bottom=True)
    render_chat_lists()

def on_chat_search(e) -> None:
    chat_search['value'] = e.value or ''
    render_chat_lists()

def build_sidebar() -> None:
    """Build the left sidebar. Chat list rendering is handled via render_chat_lists()."""
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
        render_chat_lists()

# --- conversation rendering ---
def render_messages(*, scroll_to_bottom: bool = True) -> None:
    """Render the current chat messages into the messages list container.

    During app startup there is no active NiceGUI event loop/client yet, so any JS execution
    must be guarded.
    """
    messages_list.clear()
    current = chat_messages.get(selected_chat['id'], [])

    def _stamp_with_status(m: dict) -> str:
        stamp = (m.get('stamp', '') or '').strip()
        status = m.get('status')
        # For now we only support "pending" (clock). Future: sent/received/seen.
        if status == 'pending':
            return f'{stamp}  🕒'.strip()
        return stamp

    with messages_list:
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

    # auto-scroll to bottom (scrollbar hidden but scrolling still works)
    if scroll_to_bottom:
        try:
            ui.run_javascript("""
                const el = document.getElementById('message-scroll');
                if (el) { el.scrollTop = el.scrollHeight; }
            """)
        except AssertionError:
            # Happens during startup when NiceGUI's event loop isn't ready yet.
            pass

# --- LAYOUT: simple row (sidebar + content) ---
# Lock the outer viewport to prevent an unwanted page scrollbar; internal areas scroll.
# Use h-screen so the main flex row is strictly viewport-height (important for nested scrolling).
with ui.row().classes('w-full h-screen overflow-hidden items-stretch gap-0'):
    # Sidebar (left)
    with ui.column().classes(
        'w-96 shrink-0 h-full min-h-0 flex flex-col overflow-hidden bg-[#1E1E1E] backdrop-blur-xl border-r border-white/10 px-5 py-6'
    ):
        build_sidebar()

    # Content (right)
    # min-h-0 is critical so the scrollable messages area can shrink and actually scroll
    with ui.column().classes('grow min-w-0 h-full min-h-0 overflow-hidden'):
        # Header
        # Profile header: background spans full conversation width; inner content has padding
        with ui.row().classes('w-full py-2.5 bg-[#272727] shrink-0'):
            with ui.row().classes('w-full items-center gap-3 px-6'):
                with ui.element('div').classes('w-10 h-10 rounded-full bg-white/10 border border-white/10 flex items-center justify-center'):
                    chat_avatar_initial = ui.label((_chat_by_id(selected_chat['id'])['name'][:1] or '?').upper()).classes('text-white font-semibold')
                chat_title = ui.label(_chat_by_id(selected_chat['id'])['name']).classes('text-white text-lg font-semibold')

        # Messages (scrollable; scrollbar hidden for cleaner UI)
        with ui.column().classes('flex-1 min-h-0 w-full max-w-4xl mx-auto px-5 pt-3 pb-6 message_scroll').props('id=message-scroll'):
            # Conversation start date pill (top center)
            conversation_date_pill = ui.label(_chat_by_id(selected_chat['id']).get('start_date', '')) \
                .classes('self-center mb-4 px-4 py-1 rounded-full bg-white/10 text-gray-200 text-sm')
            messages_list = ui.column().classes('w-full gap-1')
            render_messages(scroll_to_bottom=False)
    
        # Bottom input bar (inside content, pinned via layout)
        with ui.row().classes('w-full justify-center px-5 pb-6'):
            with ui.row().classes('w-full max-w-4xl mx-auto bg-[#2E2E2E] rounded-xl items-center px-4 py-2 border border-gray-700 shadow-2xl no-wrap'):
                def send_current_message() -> None:
                    text = (text_input.value or '').strip()
                    if not text:
                        return
                    chat_messages.setdefault(selected_chat['id'], []).append(
                        {'text': text, 'sent': True, 'stamp': _now_stamp(), 'status': 'pending'}
                    )
                    text_input.value = ''
                    render_messages(scroll_to_bottom=True)

                text_input = ui.input(placeholder='Send a new Message') \
                    .props('borderless dense input-class="text-gray-300 placeholder-gray-500"') \
                    .classes('grow text-base md:text-lg') \
                    .on('keydown.enter', lambda _: send_current_message())

                def add_emoji(emoji: str) -> None:
                    text_input.value = (text_input.value or '') + emoji
                    emoji_menu.close()
                    text_input.run_method('focus')

                active_category = {'value': 'Smileys'}
                search_state = {'value': ''}

                def _normalize(s: str) -> str:
                    return (s or '').strip().lower()

                def _all_emojis() -> list[str]:
                    out: list[str] = []
                    for items in EMOJI_CATEGORIES.values():
                        out.extend(items)
                    seen: set[str] = set()
                    result: list[str] = []
                    for e in out:
                        if e not in seen:
                            seen.add(e)
                            result.append(e)
                    return result

                def _filtered_emojis() -> list[str]:
                    q = _normalize(search_state['value'])
                    if not q:
                        return EMOJI_CATEGORIES.get(active_category['value'], [])
                    if q in EMOJI_ALIASES:
                        return EMOJI_ALIASES[q]
                    all_list = _all_emojis()
                    if any(q in e for e in all_list):
                        return [e for e in all_list if q in e][:120]
                    return []

                with ui.button().props('flat round dense icon=emoji_emotions').classes('text-white hover:bg-white/10 transition-colors mr-2'):
                    with ui.menu().classes('shadow-2xl') as emoji_menu:
                        with ui.card().classes('emoji_picker_card bg-[#1f1f1f] text-gray-100 border border-gray-700 p-2'):
                            ui.element('div').style('width: 520px; max-width: 520px;')

                            with ui.row().classes('emoji_cat_strip items-center'):
                                for name in EMOJI_CATEGORIES.keys():
                                    with ui.button(
                                        on_click=lambda name=name: (
                                            active_category.__setitem__('value', name),
                                            search_state.__setitem__('value', ''),
                                            search_input.set_value(''),
                                            render_emojis(),
                                        ),
                                    ).props('flat dense').classes('text-gray-200 hover:bg-white/10 rounded-lg px-2 py-1'):
                                        ui.html(CATEGORY_SVGS.get(name, ''), sanitize=False).classes('text-gray-200')
                                        ui.tooltip(name)

                            search_input = ui.input(placeholder='Search (e.g. love, lol, party, fire)…') \
                                .props('dense borderless input-class="text-gray-100 placeholder-gray-500"') \
                                .classes('w-full bg-[#2a2a2a] rounded-lg px-2 mt-2')

                            status = ui.label('').classes('text-gray-400 text-xs mt-1')

                            grid_container = ui.element('div').classes('emoji_grid w-full mt-2')
                            grid_container.style('max-height: 280px; overflow-y: auto; padding: 2px;')

                            def render_emojis() -> None:
                                emojis = _filtered_emojis()
                                grid_container.clear()
                                if _normalize(search_state['value']) and not emojis:
                                    status.set_text('No results')
                                else:
                                    status.set_text(active_category['value'] if not _normalize(search_state['value']) else 'Search results')

                                with grid_container:
                                    grid = ui.element('div').classes('grid gap-1 w-full')
                                    grid.style('grid-template-columns: repeat(10, minmax(0, 1fr));')
                                    with grid:
                                        for e in emojis:
                                            ui.button(e, on_click=lambda e=e: add_emoji(e)) \
                                                .props('flat dense') \
                                                .classes('emoji_btn text-xl text-gray-100 hover:bg-white/10 rounded-lg')

                            def on_search_change(e) -> None:
                                search_state['value'] = e.value or ''
                                render_emojis()

                            search_input.on_value_change(on_search_change)
                            render_emojis()

                with ui.button(on_click=send_current_message).props('flat round dense icon=send').classes('text-white hover:bg-white/10 transition-colors ml-2'):
                    pass

ui.run(native=True, window_size=(1500, 750), title="Rift")