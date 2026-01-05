from __future__ import annotations

from nicegui import ui


DEFAULT_LOADING_MESSAGES: list[str] = [
    "Warming up the servers…",
    "Lining up your recent chats…",
    "Polishing pixels…",
    "Fetching fresh vibes…",
    "Connecting the dots…",
    "Synchronizing messages…",
    "Almost there — hang tight…",
    "Brewing a fresh session…",
    "Reticulating splines…",
    "Making everything feel snappy…",
]


def build_loading_screen(
    *,
    title: str = "Loading...",
    subtitle: str = "Preparing your chats...",
    rotating_messages: list[str] | None = None,
) -> ui.element:
    """Full-screen loading view (simple centered logo + text)."""

    root = ui.element("div").classes("w-full h-screen flex items-center justify-center").style(
        "background-color: #1a1a1a;"
        "background-image: none;"
        "margin: 0;"
        "padding: 0;"
        "overflow: hidden;"
    )

    with root:
        with ui.column().classes("items-center text-center gap-3 px-6"):
            ui.image("/static/thick_logo.svg").classes("w-16 h-16 md:w-20 md:h-20 opacity-90")
            ui.label(title).classes("text-white text-4xl md:text-5xl font-semibold tracking-tight")
            subtitle_label = ui.label(subtitle).classes("text-gray-400 text-lg md:text-xl w-full text-center")

            messages = rotating_messages or DEFAULT_LOADING_MESSAGES
            if messages:
                idx = {'value': 0}

                def _rotate_message() -> None:
                    idx['value'] = (idx['value'] + 1) % len(messages)
                    subtitle_label.set_text(messages[idx['value']])

                # Swap the secondary line every 5 seconds to keep the screen lively.
                ui.timer(5.0, _rotate_message)

    return root


