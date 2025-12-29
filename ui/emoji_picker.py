from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from nicegui import app, ui


@dataclass(frozen=True)
class EmojiCategory:
    key: str
    tab_label: str  # keep tabs compact (emoji icon)
    name: str
    emojis: List[str]


_CATEGORIES: List[EmojiCategory] = [
    EmojiCategory(
        key="recent",
        tab_label="🕘",
        name="Recent",
        emojis=[],
    ),
    EmojiCategory(
        key="smileys",
        tab_label="😀",
        name="Smileys",
        emojis=[
            "😀", "😃", "😄", "😁", "😆", "😅", "🤣", "😂", "🙂", "🙃", "😉", "😊",
            "😇", "🥰", "😍", "🤩", "😘", "😗", "☺️", "😚", "😙", "🥲", "😋", "😛",
            "😜", "🤪", "😝", "🤑", "🤗", "🤭", "🫢", "🫣", "🤫", "🤔", "🫡", "🤐",
            "🤨", "😐", "😑", "😶", "🫥", "😶‍🌫️", "🙄", "😏", "😣", "😥", "😮", "🤯",
            "😳", "🥵", "🥶", "😱", "😨", "😰", "😢", "😭", "😤", "😠", "😡", "🤬",
            "🤕", "🤒", "😷", "🤢", "🤮", "🥴", "😵", "😵‍💫", "🤧", "😴", "🥱", "😪",
            "😮‍💨", "😬", "😓", "🫠", "🤥", "😈", "👿", "💀", "☠️", "👻", "👽", "🤖",
            "🎃", "😺", "😸", "😹", "😻", "😼", "😽", "🙀", "😿", "😾",
        ],
    ),
    EmojiCategory(
        key="gestures",
        tab_label="👍",
        name="Gestures",
        emojis=[
            "👍", "👎", "👌", "🤌", "🤏", "✌️", "🤞", "🫰", "🤟", "🤘", "🤙", "👈",
            "👉", "👆", "👇", "☝️", "🫵", "✋", "🤚", "🖐️", "🖖", "👋", "🤝", "🙏",
            "👏", "🫶", "🙌", "👐", "🤲", "🤜", "🤛", "✊", "👊", "🫳", "🫴", "💪",
            "🦾", "🖕", "✍️", "🤳", "💅",
        ],
    ),
    EmojiCategory(
        key="people",
        tab_label="🧑",
        name="People",
        emojis=[
            "🧑", "👩", "👨", "🧑‍🦰", "👩‍🦰", "👨‍🦰", "🧑‍🦱", "👩‍🦱", "👨‍🦱",
            "🧑‍🦳", "👩‍🦳", "👨‍🦳", "🧑‍🦲", "👩‍🦲", "👨‍🦲", "👶", "🧒", "👦", "👧",
            "🧓", "👴", "👵", "🧔", "🧔‍♂️", "🧔‍♀️", "👱", "👱‍♂️", "👱‍♀️",
            "🕵️", "🕵️‍♂️", "🕵️‍♀️", "👷", "👷‍♂️", "👷‍♀️", "👮", "👮‍♂️", "👮‍♀️",
            "🧑‍⚕️", "👩‍⚕️", "👨‍⚕️", "🧑‍🎓", "👩‍🎓", "👨‍🎓",
            "🧑‍💻", "👩‍💻", "👨‍💻", "🧑‍🏫", "👩‍🏫", "👨‍🏫",
            "🧑‍🍳", "👩‍🍳", "👨‍🍳", "🧑‍🚒", "👩‍🚒", "👨‍🚒",
            "🧑‍🚀", "👩‍🚀", "👨‍🚀", "🧑‍⚖️", "👩‍⚖️", "👨‍⚖️",
            "🧑‍🎤", "👩‍🎤", "👨‍🎤", "🧑‍🎨", "👩‍🎨", "👨‍🎨",
            "🧑‍🔧", "👩‍🔧", "👨‍🔧", "🧑‍🏭", "👩‍🏭", "👨‍🏭",
            "🧑‍🚜", "👩‍🚜", "👨‍🚜", "🧑‍💼", "👩‍💼", "👨‍💼",
        ],
    ),
    EmojiCategory(
        key="hearts",
        tab_label="❤️",
        name="Hearts",
        emojis=[
            "❤️", "🩷", "🧡", "💛", "💚", "🩵", "💙", "💜", "🖤", "🩶", "🤍", "🤎",
            "💔", "❤️‍🔥", "❤️‍🩹", "💕", "💞", "💓", "💗", "💖", "💘", "💝", "💟",
            "❣️", "💌",
        ],
    ),
    EmojiCategory(
        key="animals",
        tab_label="🐶",
        name="Animals",
        emojis=[
            "🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐻‍❄️", "🐨", "🐯", "🦁",
            "🐮", "🐷", "🐽", "🐸", "🐵", "🙈", "🙉", "🙊", "🐒", "🐔", "🐧", "🐦",
            "🐤", "🐣", "🐥", "🦆", "🦅", "🦉", "🦇", "🐺", "🐗", "🐴", "🦄", "🐝",
            "🪲", "🦋", "🐌", "🐞", "🪳", "🪰", "🪱", "🕷️", "🕸️", "🦂", "🐢", "🐍",
            "🦎", "🐙", "🦑", "🦐", "🦞", "🦀", "🐡", "🐠", "🐟", "🐬", "🐳", "🐋",
            "🦈", "🐊", "🐅", "🐆", "🦓", "🦍", "🦧", "🐘", "🦛", "🦏", "🐪", "🐫",
            "🦒", "🦘", "🦬", "🐃", "🐂", "🐄", "🐎", "🐖", "🐏", "🐑", "🦙", "🐐",
            "🦌", "🐕", "🐩", "🦮", "🐕‍🦺", "🐈", "🐈‍🦺",
        ],
    ),
    EmojiCategory(
        key="food",
        tab_label="🍕",
        name="Food",
        emojis=[
            "🍏", "🍎", "🍐", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🫐", "🍈", "🍒",
            "🍑", "🥭", "🍍", "🥥", "🥝", "🍅", "🍆", "🥑", "🥦", "🥬", "🥒", "🌶️",
            "🫑", "🌽", "🥕", "🫒", "🧄", "🧅", "🥔", "🍠", "🥐", "🥯", "🍞", "🥖",
            "🥨", "🧀", "🥚", "🍳", "🧈", "🥞", "🧇", "🥓", "🥩", "🍗", "🍖", "🦴",
            "🌭", "🍔", "🍟", "🍕", "🥪", "🥙", "🧆", "🌮", "🌯", "🥗", "🥘", "🍝",
            "🍜", "🍲", "🍛", "🍣", "🍱", "🥟", "🦪", "🍤", "🍙", "🍚", "🍘", "🍥",
            "🥠", "🥮", "🍢", "🍡", "🍧", "🍨", "🍦", "🥧", "🧁", "🍰", "🎂", "🍮",
            "🍭", "🍬", "🍫", "🍿", "🍩", "🍪", "🥛", "🍼", "☕", "🫖", "🍵", "🍶",
            "🍺", "🍻", "🥂", "🍷", "🥃", "🍸", "🍹", "🧉", "🍾",
        ],
    ),
    EmojiCategory(
        key="activities",
        tab_label="⚽",
        name="Activities",
        emojis=[
            "⚽", "🏀", "🏈", "⚾", "🥎", "🎾", "🏐", "🏉", "🥏", "🎱", "🏓", "🏸",
            "🥅", "🏒", "🏑", "🏏", "⛳", "🪁", "🥊", "🥋", "🛹", "🛼", "🛷", "⛸️",
            "🥌", "🎿", "⛷️", "🏂", "🪂", "🏋️", "🏋️‍♂️", "🏋️‍♀️", "🤼", "🤼‍♂️", "🤼‍♀️",
            "🤸", "🤸‍♂️", "🤸‍♀️", "⛹️", "⛹️‍♂️", "⛹️‍♀️", "🤺", "🤾", "🤾‍♂️", "🤾‍♀️",
            "🏌️", "🏌️‍♂️", "🏌️‍♀️", "🏇", "🧘", "🧘‍♂️", "🧘‍♀️", "🎮", "🎲", "🎯",
            "🎳", "🎣", "🎨", "🎭", "🎤", "🎧", "🎸", "🎹", "🥁", "🎷", "🎺", "🎻",
            "🎬", "🎟️", "🎫",
        ],
    ),
    EmojiCategory(
        key="travel",
        tab_label="✈️",
        name="Travel",
        emojis=[
            "🚗", "🚕", "🚙", "🚌", "🚎", "🏎️", "🚓", "🚑", "🚒", "🚐", "🛻", "🚚",
            "🚛", "🚜", "🛵", "🏍️", "🚲", "🛴", "🚨", "🚔", "🚍", "🚘", "🚖", "🚡",
            "🚠", "🚟", "🚃", "🚋", "🚞", "🚝", "🚄", "🚅", "🚈", "🚂", "🚆", "🚇",
            "🚊", "🚉", "✈️", "🛫", "🛬", "🛩️", "💺", "🛰️", "🚀", "🛸", "🚁", "🛶",
            "⛵", "🚤", "🛥️", "🛳️", "⛴️", "🚢", "⚓", "🗺️", "🧭", "⛰️", "🏔️", "🗻",
            "🏕️", "🏖️", "🏜️", "🏝️", "🏞️", "🏟️", "🏛️", "🏗️", "🧱", "🪨", "🏘️", "🏠",
            "🏡", "🏢", "🏣", "🏤", "🏥", "🏦", "🏨", "🏩", "🏪", "🏫", "🏬", "🏭",
            "🗼", "🗽", "⛩️", "🕌", "🕍", "⛪", "🛤️", "🌉", "🌁",
        ],
    ),
    EmojiCategory(
        key="objects",
        tab_label="💡",
        name="Objects",
        emojis=[
            "⌚", "📱", "📲", "💻", "⌨️", "🖥️", "🖨️", "🖱️", "🖲️", "🕹️", "💿", "📀",
            "📷", "📸", "📹", "🎥", "📽️", "🎞️", "📞", "☎️", "📟", "📠", "📺", "📻",
            "🧭", "⏱️", "⏲️", "⏰", "🕰️", "⌛", "⏳", "📡", "🔋", "🪫", "🔌", "💡",
            "🔦", "🕯️", "🪔", "🧯", "🛢️", "💸", "💵", "💴", "💶", "💷", "🪙", "💰",
            "💳", "🧾", "🪪", "🔑", "🗝️", "🚪", "🪞", "🪟", "🛏️", "🛋️", "🪑", "🚽",
            "🪠", "🚿", "🛁", "🧴", "🧷", "🧹", "🧺", "🧻", "🪣", "🧼", "🪥", "🪒",
            "🧽", "🪜", "🧲", "🪝", "🧰", "🪛", "🔧", "🔨", "🪓", "⛏️", "⚒️", "🛠️",
            "🗡️", "⚔️", "🔫", "🪃", "🏹", "🛡️", "🪚", "🔩", "⚙️", "🪤", "🧱",
            "📌", "📍", "✂️", "🖊️", "🖋️", "✒️", "📝", "📒", "📓", "📔", "📕", "📗",
            "📘", "📙", "📚", "📖", "🔖", "🗂️", "📁", "📂", "🗃️", "🗄️", "🗑️",
        ],
    ),
    EmojiCategory(
        key="symbols",
        tab_label="✨",
        name="Symbols",
        emojis=[
            "✨", "💫", "⭐", "🌟", "⚡", "🔥", "💥", "☄️", "🌈", "☀️", "🌤️", "⛅",
            "🌥️", "☁️", "🌦️", "🌧️", "⛈️", "🌩️", "🌨️", "❄️", "☃️", "⛄", "💨", "🌪️",
            "🌫️", "🌊", "💧", "💦", "🫧", "🎉", "🎊", "🎈", "🎁", "🏆", "🥇", "🥈",
            "🥉", "✅", "☑️", "✔️", "❌", "❎", "➕", "➖", "➗", "✖️", "♻️", "🔁",
            "🔂", "🔄", "🔃", "🔺", "🔻", "🔸", "🔹", "🔶", "🔷", "🔴", "🟠", "🟡",
            "🟢", "🔵", "🟣", "⚫", "⚪", "🟤", "🔔", "🔕", "🔊", "🔉", "🔈", "🔇",
            "🔒", "🔓", "🔏", "🔐", "⚠️", "🚫", "⛔", "🛑", "💯",
        ],
    ),
]


def _normalize(s: str) -> str:
    return (s or "").strip().lower()


def _recent_emojis() -> List[str]:
    # user-scoped storage (works for native + web)
    storage = getattr(app, "storage", None)
    if storage is not None and hasattr(storage, "user"):
        return list(storage.user.get("recent_emojis", []))
    # Fallback for older/newer APIs (if present)
    ui_storage = getattr(ui, "storage", None)
    if ui_storage is not None and hasattr(ui_storage, "user"):
        return list(ui_storage.user.get("recent_emojis", []))
    return []


def _push_recent(emoji: str, limit: int = 32) -> None:
    recent = [e for e in _recent_emojis() if e != emoji]
    recent.insert(0, emoji)
    storage = getattr(app, "storage", None)
    if storage is not None and hasattr(storage, "user"):
        storage.user["recent_emojis"] = recent[:limit]
        return
    ui_storage = getattr(ui, "storage", None)
    if ui_storage is not None and hasattr(ui_storage, "user"):
        ui_storage.user["recent_emojis"] = recent[:limit]


def attach_emoji_picker(
    *,
    text_input: ui.input,
    button_classes: str = "text-white hover:bg-white/10 transition-colors mr-2",
    menu_width_px: int = 288,
    grid_cols: int = 8,
    grid_max_height_px: int = 260,
) -> None:
    """Attach a compact, dark-themed emoji picker that inserts into a NiceGUI input."""

    # Add once: hide scrollbars for our emoji grid while keeping scrolling.
    if not getattr(attach_emoji_picker, "_css_added", False):
        ui.add_head_html(
            """
<style>
/* Hide scrollbars inside the emoji picker while keeping scroll behavior (scoped). */
.emoji-picker, .emoji-picker * {
  scrollbar-width: none !important;         /* Firefox */
  -ms-overflow-style: none !important;      /* IE/Edge legacy */
}
.emoji-picker *::-webkit-scrollbar {
  width: 0 !important;
  height: 0 !important;
  display: none !important;                 /* Chromium/WebKit */
}
/* Quasar scroll area bars (NiceGUI uses Quasar under the hood) */
.emoji-picker .q-scrollarea__bar,
.emoji-picker .q-scrollarea__thumb {
  opacity: 0 !important;
  width: 0 !important;
  height: 0 !important;
  display: none !important;
}
/* Category strip: keep on one line and hide horizontal scrollbar */
.emoji-picker .emoji-category-strip {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
  overflow-y: hidden;
  gap: 4px;
}
</style>
            """.strip()
        )
        setattr(attach_emoji_picker, "_css_added", True)

    menu: Optional[ui.menu] = None
    search_value = {"value": ""}
    active_category = {"value": "smileys"}
    panel_container: Optional[ui.element] = None

    def close_menu() -> None:
        nonlocal menu
        if menu is not None:
            menu.close()

    def insert_emoji(emoji: str) -> None:
        text_input.value = (text_input.value or "") + emoji
        _push_recent(emoji)
        render()  # update "Recent"
        close_menu()
        text_input.run_method("focus")

    def filtered_emojis() -> List[str]:
        q = _normalize(search_value["value"])
        if not q:
            for c in _CATEGORIES:
                if c.key == active_category["value"]:
                    if c.key == "recent":
                        return _recent_emojis()
                    return c.emojis
            return []

        # Search across all categories (excluding recent)
        all_emojis: List[str] = []
        for c in _CATEGORIES:
            if c.key == "recent":
                continue
            all_emojis.extend(c.emojis)

        # Basic search: unicode names aren't available offline; use a small alias map
        aliases: Dict[str, List[str]] = {
            "lol": ["😂", "🤣"],
            "laugh": ["😂", "🤣", "😆", "😄"],
            "cry": ["😭", "😢"],
            "sad": ["😢", "😭", "😔", "😞"],
            "angry": ["😡", "😠", "🤬"],
            "love": ["❤️", "😍", "😘", "🥰", "💖", "💕"],
            "fire": ["🔥"],
            "party": ["🥳", "🎉", "🎊"],
            "ok": ["👌"],
            "thumbs": ["👍", "👎"],
            "clap": ["👏"],
            "pray": ["🙏"],
            "think": ["🤔"],
            "cool": ["😎"],
        }
        if q in aliases:
            return aliases[q]

        # If user types an emoji itself, just show it
        if len(q) <= 3 and any(q in e for e in all_emojis):
            return [e for e in all_emojis if q in e][:64]

        # No name metadata => fallback to "no results"
        return []

    def render() -> None:
        nonlocal panel_container
        if panel_container is None:
            return
        panel_container.clear()

        emojis = filtered_emojis()
        q = _normalize(search_value["value"])

        with panel_container:
            if q and not emojis:
                ui.label("No results").classes("text-gray-400 text-sm px-1")
                return

            # Grid (Quasar scroll area so we can reliably hide scrollbars)
            scroll = ui.element("q-scroll-area").classes("w-full")
            scroll.props(
                'thumb-style="opacity:0;width:0px" bar-style="opacity:0;width:0px"'
            )
            scroll.style(f"height: {grid_max_height_px}px;")
            with scroll:
                grid = ui.element("div").classes(
                    f"grid gap-1 w-full"
                ).style(
                    f"grid-template-columns: repeat({grid_cols}, minmax(0, 1fr)); padding: 2px;"
                )
                with grid:
                    for e in emojis:
                        ui.button(
                            e,
                            on_click=lambda e=e: insert_emoji(e),
                        ).props("flat dense").classes(
                            "text-xl text-gray-100 hover:bg-white/10"
                        ).style(
                            "min-width: 34px; height: 34px;"
                        )

    def set_category(key: str) -> None:
        active_category["value"] = key
        render()

    def on_search_change(e) -> None:
        search_value["value"] = e.value or ""
        render()

    # Button + Menu UI
    with ui.button().props("flat round dense icon=emoji_emotions").classes(button_classes):
        with ui.menu().classes("shadow-2xl") as m:
            menu = m
            with ui.card().classes("emoji-picker bg-[#1f1f1f] text-gray-100 border border-gray-700").style(
                f"width: {menu_width_px}px; max-width: {menu_width_px}px; overflow: hidden;"
            ):
                # Header
                with ui.column().classes("gap-2 p-2"):
                    # Compact category strip (emoji-only tabs)
                    with ui.row().classes("emoji-category-strip items-center"):
                        for c in _CATEGORIES:
                            ui.button(
                                c.tab_label,
                                on_click=lambda c=c: set_category(c.key),
                            ).props("flat dense").classes(
                                "text-lg text-gray-100 hover:bg-white/10"
                            ).style("min-width: 34px; height: 34px;")

                    ui.input(placeholder="Search (e.g. love, lol, fire)…") \
                        .props('dense borderless input-class="text-gray-100 placeholder-gray-500"') \
                        .classes("w-full bg-[#2a2a2a] rounded-lg px-2") \
                        .on_value_change(on_search_change)

                    panel_container = ui.element("div").classes("pt-1")
                    render()


