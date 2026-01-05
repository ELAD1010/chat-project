from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from nicegui import ui

from category_svgs import CATEGORY_SVGS
from emoji_data import EMOJI_ALIASES, EMOJI_CATEGORIES


@dataclass
class BottomInputBarRefs:
    text_input: ui.input


def build_bottom_input_bar(*, on_send: Callable[[str], None]) -> BottomInputBarRefs:
    """Bottom input bar (text input + emoji picker + send). Calls on_send(text) when user sends."""

    with ui.row().classes('w-full max-w-4xl mx-auto bg-[#2E2E2E] rounded-xl items-center px-4 py-2 border border-gray-700 shadow-2xl no-wrap'):
        def send_current_message() -> None:
            text = (text_input.value or '').strip()
            if not text:
                return
            on_send(text)
            text_input.value = ''

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

    return BottomInputBarRefs(text_input=text_input)


