from __future__ import annotations

from pathlib import Path

from nicegui import ui


def build_welcome_view(
    *,
    title: str = "Welcome",
    subtitle: str = "We missed you!",
    logo_svg_path: str | None = None,
) -> ui.element:
    """Build the right-side welcome screen (WhatsApp Web style).

    Note: This intentionally uses a solid background (no wallpaper SVG decoration).
    """
    svg_path = Path(logo_svg_path) if logo_svg_path else (Path(__file__).resolve().parent / "logo.svg")
    svg = ""
    try:
        svg = svg_path.read_text(encoding="utf-8")
    except OSError:
        svg = ""

    root = ui.element("div").classes(
        "w-full h-full flex items-center justify-center"
    ).style(
        "background-color: #1a1a1a;"
        "background-image: none;"
    )

    with root:
        with ui.column().classes("items-center justify-center gap-3 text-center px-6"):
            if svg:
                ui.html(svg, sanitize=False).classes("w-16 h-16 opacity-90")
            ui.label(title).classes("text-white text-4xl font-semibold tracking-tight")
            ui.label(subtitle).classes("text-gray-400 text-lg")

    return root


