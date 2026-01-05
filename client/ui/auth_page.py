from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from nicegui import ui


_AUTH_CSS_ADDED = False


@dataclass(frozen=True)
class AuthTheme:
    background: str = 'url("/static/gradient.svg")'
    card_bg: str = "#1E1E1E"
    input_bg: str = "#2A2A2A"
    primary: str = "#FFFFFF"
    secondary: str = "#9CA3AF"
    accent: str = "#6600FF"


def _ensure_auth_css() -> None:
    global _AUTH_CSS_ADDED
    if _AUTH_CSS_ADDED:
        return

    ui.add_head_html(
        """
<style>
  /* Scoped to auth inputs only */
  .auth_input_wrap .q-field__native {
    padding: 12px 14px !important;
    font-size: 16px !important;
    line-height: 24px !important;
  }
  .auth_input_wrap input::placeholder {
    font-size: 14px !important;
    color: #6B7280 !important;
  }
  /* Password eye toggle */
  .auth_input_wrap .q-field__append,
  .auth_input_wrap .q-field__append *,
  .auth_input_wrap .q-icon,
  .auth_input_wrap .q-btn,
  .auth_input_wrap .q-btn .q-icon,
  .auth_input_wrap .text-black,
  .auth_input_wrap .text-dark {
    color: #FFFFFF !important;
  }
  .auth_input_wrap .q-field__append {
    padding-right: 14px !important;
    margin-left: 6px !important;
  }
  .auth_input_wrap .q-field__control {
    padding-right: 14px !important;
  }
  .auth_input_wrap {
    padding-right: 14px !important;
    box-sizing: border-box;
  }
  .auth_input_wrap .q-field__append .q-btn,
  .auth_input_wrap .q-field__append .q-icon {
    margin-right: 10px !important;
  }
</style>
        """.strip()
    )
    _AUTH_CSS_ADDED = True


def build_auth_page(
    *,
    title: str,
    subtitle: str,
    primary_button_text: str,
    on_primary: Optional[Callable[[str, str], dict]] = None,
    on_success: Optional[Callable[[dict], None]] = None,
    footer_prefix: str,
    footer_action_text: str,
    on_footer_action: Optional[Callable[[], None]] = None,
    theme: AuthTheme = AuthTheme(),
) -> ui.element:
    _ensure_auth_css()

    root = ui.element("div").classes(
        "w-full h-screen relative flex items-center justify-center overflow-hidden"
    ).style(
        f"background-image: {theme.background};"
        "background-size: cover;"
        "background-position: center;"
        "background-attachment: fixed;"
        "margin: 0;"
        "padding: 0;"
    )

    with root:
        # top-left brand
        with ui.row().classes("absolute top-10 left-10 items-center gap-4"):
            ui.label("Rift").classes("text-white text-3xl font-semibold tracking-tight")
            ui.image("/static/thick_logo.svg").classes("w-10 h-10")

        with ui.card().classes(
            "w-[720px] max-w-[92vw] rounded-2xl shadow-2xl border border-white/5"
        ).style(f"background-color: {theme.card_bg};"):
            with ui.column().classes("w-full p-8 sm:p-10 md:p-12"):
                with ui.column().classes("gap-1"):
                    ui.label(title).classes("text-white text-4xl font-semibold")
                    ui.label(subtitle).classes("text-gray-400 text-base")

                ui.element("div").classes("h-6")

                def _field(label: str, icon_src: str, placeholder: str, *, password: bool = False) -> ui.input:
                    with ui.column().classes("w-full gap-2"):
                        with ui.row().classes("items-center gap-2"):
                            ui.image(icon_src).classes("w-5 h-5")
                            ui.label(label).classes("text-gray-200 text-base")

                        with ui.element("div").classes("auth_input_wrap w-full rounded-xl border border-white/10").style(
                            f"background-color: {theme.input_bg};"
                        ):
                            inp = ui.input(placeholder=placeholder, password=password, password_toggle_button=password) \
                                .props(
                                    'borderless dense dark '
                                    'input-style="padding: 12px 14px; font-size: 16px; line-height: 24px;" '
                                    'input-class="text-gray-200 placeholder-gray-500"'
                                ) \
                                .classes("w-full")
                        return inp

                with ui.column().classes("w-full gap-6"):
                    email_input = _field("Email", "/static/email.svg", "johndoe@gmail.com")
                    password_input = _field("Password", "/static/password.svg", '"1234" isn’t a strong password, Kevin.', password=True)

                    error_label = ui.label('').classes('text-red-500 text-sm hidden')

                    def _do_primary() -> None:
                        if on_primary:
                            try:
                                result = on_primary((email_input.value or '').strip(), (password_input.value or '')) or {}
                                status = (result.get('status') or '').lower()
                                message = (result.get('message') or '').strip()
                                if status == 'success':
                                    error_label.set_text('')
                                    error_label.classes(add='hidden')
                                    if on_success:
                                        on_success(result)
                                else:
                                    error_label.set_text(message or 'Something went wrong.')
                                    error_label.classes(remove='hidden')
                            except Exception:
                                error_label.set_text('Something went wrong.')
                                error_label.classes(remove='hidden')

                    # Allow submitting with Enter from either field (best UX for auth forms)
                    email_input.on('keydown.enter', lambda _: _do_primary())
                    password_input.on('keydown.enter', lambda _: _do_primary())

                    ui.button(primary_button_text, on_click=_do_primary) \
                        .props("unelevated") \
                        .classes("w-full rounded-xl py-4 text-lg font-medium") \
                        .style(f"background-color: {theme.accent} !important; color: {theme.primary} !important;")

                    with ui.row().classes("items-center gap-1"):
                        ui.label(footer_prefix).classes("text-white text-sm")
                        action = ui.label(footer_action_text).classes("text-sm cursor-pointer").style(
                            f"color: {theme.accent};"
                        )
                        if on_footer_action:
                            def _footer_click(_) -> None:
                                error_label.set_text('')
                                error_label.classes(add='hidden')
                                on_footer_action()

                            action.on("click", _footer_click)

    return root


