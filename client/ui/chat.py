import asyncio

from nicegui import app, ui
from login_ui import build_login_page
from register_ui import build_register_page
from authentication import login as auth_login
from authentication import register as auth_register
from app_state import load_chat_data, loading_state, selected_chat
from styles import apply_global_css, set_body_background
from sidebar import build_sidebar, render_chat_lists
from bottom_input_bar import build_bottom_input_bar
from chat_layout import build_chat_content
from loading_ui import build_loading_screen

# --- SETUP BACKGROUND ---
app.add_static_files('/static', 'client/ui/assets')
apply_global_css()
set_body_background(background_url="/static/gradient.svg")

sidebar_refs = None
chat_layout_refs = {'value': None}

def select_chat(chat_id: str) -> None:
    # Proxy: sidebar clicks happen after layout is built; delegate to chat_layout's handler.
    if chat_layout_refs['value'] is not None:
        chat_layout_refs['value'].on_select_chat(chat_id)

def render_messages(*, scroll_to_bottom: bool = True) -> None:
    # Kept for compatibility with earlier structure; chat_layout owns rendering now.
    if chat_layout_refs['value'] is not None:
        from messages_view import render_messages as _render

        _render(chat_layout_refs['value'].messages_refs, scroll_to_bottom=scroll_to_bottom)

# --- LAYOUT: simple row (sidebar + content) ---
# Lock the outer viewport to prevent an unwanted page scrollbar; internal areas scroll.
# Use h-screen so the main flex row is strictly viewport-height (important for nested scrolling).
def _show_app() -> None:
    try:
        login_view.classes(add='hidden')
        register_view.classes(add='hidden')
        loading_view.classes(add='hidden')
        app_view.classes(remove='hidden')
    except Exception:
        pass


def _on_auth_success(result: dict) -> None:
    # Show loading screen immediately, then load data asynchronously.
    loading_state['value'] = True
    try:
        login_view.classes(add='hidden')
        register_view.classes(add='hidden')
        app_view.classes(add='hidden')
        loading_view.classes(remove='hidden')
    except Exception:
        pass

    async def _load() -> None:
        # TESTING ONLY: simulate network delay; remove once real API is wired.
        await asyncio.sleep(2)

        user_id = (result.get('user_id') or 'demo')
        load_chat_data(str(user_id))
        if sidebar_refs:
            render_chat_lists(chat_list_containers=sidebar_refs.chat_list_containers, on_select_chat=select_chat)
        _show_app()

    asyncio.create_task(_load())


def _show_login() -> None:
    try:
        register_view.classes(add='hidden')
        loading_view.classes(add='hidden')
        login_view.classes(remove='hidden')
    except Exception:
        pass


def _show_register() -> None:
    try:
        login_view.classes(add='hidden')
        loading_view.classes(add='hidden')
        register_view.classes(remove='hidden')
    except Exception:
        pass


# Login page is the default entry for now
login_view = build_login_page(on_login=auth_login, on_success=_on_auth_success, on_show_register=_show_register)
register_view = build_register_page(on_register=auth_register, on_success=_on_auth_success, on_show_login=_show_login)
register_view.classes(add='hidden')

# Loading screen (hidden by default)
loading_view = build_loading_screen()
loading_view.classes(add='hidden')

# Chat app view (hidden until login)
app_view = ui.element('div').classes('w-full h-screen overflow-hidden hidden').style(
    'background-image: url("/static/wallpaper.svg");'
    'background-size: cover;'
    'background-position: center;'
    'background-attachment: fixed;'
    'background-color: #1a1a1a;'
)

with app_view:
    with ui.row().classes('w-full h-screen overflow-hidden items-stretch gap-0'):
        # Sidebar (left)
        with ui.column().classes(
            'w-96 shrink-0 h-full min-h-0 flex flex-col overflow-hidden bg-[#1E1E1E] backdrop-blur-xl border-r border-white/10 px-5 py-6'
        ):
            sidebar_refs = build_sidebar(on_select_chat=select_chat)

        # Content (right)
        # min-h-0 is critical so the scrollable messages area can shrink and actually scroll
        with ui.column().classes('grow min-w-0 h-full min-h-0 overflow-hidden'):
            chat_layout_refs['value'] = build_chat_content(
                sidebar_refs=sidebar_refs,
                build_composer_row=lambda on_send: build_bottom_input_bar(on_send=on_send),
            )

ui.run(native=True, window_size=(1500, 750), title="Rift")