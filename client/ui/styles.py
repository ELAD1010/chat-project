from __future__ import annotations

from nicegui import ui


GLOBAL_CSS = """
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


def apply_global_css() -> None:
    ui.add_head_html(GLOBAL_CSS)


def set_body_background(*, background_url: str, background_color: str = "#1a1a1a") -> None:
    ui.query('body').style(
        f'background-image: url("{background_url}");'
        'background-size: cover;'
        'background-position: center;'
        'background-attachment: fixed;'
        f'background-color: {background_color};'
        'margin: 0;'
        'padding: 0;'
        'overflow: hidden;'
    )


