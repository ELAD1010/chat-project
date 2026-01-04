from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from nicegui import ui

_LOGIN_CSS_ADDED = False


@dataclass(frozen=True)
class LoginTheme:
    background: str = 'url("/static/gradient.svg")'
    card_bg: str = "#1E1E1E"
    input_bg: str = "#2A2A2A"
    primary: str = "#FFFFFF"
    secondary: str = "#9CA3AF"  # gray-400-ish
    accent: str = "#6600FF"


def build_login_page(
    *,
    on_login: Optional[Callable[[], None]] = None,
    theme: LoginTheme = LoginTheme(),
) -> ui.element:
    global _LOGIN_CSS_ADDED
    if not _LOGIN_CSS_ADDED:
        ui.add_head_html(
            """
<style>
  /* Scoped to login inputs only */
  .login_input_wrap .q-field__native {
    padding: 12px 14px !important;
    font-size: 16px !important;
    line-height: 24px !important;
  }
  .login_input_wrap input::placeholder {
    font-size: 14px !important;
    color: #6B7280 !important; /* secondary gray */
  }
  /* Password eye toggle (Quasar append area) */
  .login_input_wrap .q-field__append,
  .login_input_wrap .q-field__append *,
  .login_input_wrap .q-icon,
  .login_input_wrap .q-btn,
  .login_input_wrap .q-btn .q-icon,
  .login_input_wrap .text-black,
  .login_input_wrap .text-dark {
    color: #FFFFFF !important;
  }
  /* Give the append (eye icon) breathing room from the right edge */
  .login_input_wrap .q-field__append {
    padding-right: 14px !important;
    margin-left: 6px !important;
  }
  /* Inset the whole control content from the right edge (more reliable for Quasar) */
  .login_input_wrap .q-field__control {
    padding-right: 14px !important;
  }
  /* Fallback: pad the wrapper itself so the entire QInput (incl. eye) is inset from the border */
  .login_input_wrap {
    padding-right: 14px !important;
    box-sizing: border-box;
  }
  /* Extra fallback: add breathing room on the actual toggle button/icon */
  .login_input_wrap .q-field__append .q-btn,
  .login_input_wrap .q-field__append .q-icon {
    margin-right: 10px !important;
  }
</style>
            """.strip()
        )
        _LOGIN_CSS_ADDED = True

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

        # centered card
        with ui.card().classes(
            "w-[720px] max-w-[92vw] rounded-2xl shadow-2xl border border-white/5"
        ).style(
            f"background-color: {theme.card_bg};"
        ):
            # responsive padding block (64px target, scaled down on small screens)
            with ui.column().classes("w-full p-8 sm:p-10 md:p-12"):
                with ui.column().classes("gap-1"):
                    ui.label("Welcome Back!").classes("text-white text-4xl font-semibold")
                    ui.label("We missed you!").classes("text-gray-400 text-base")

                ui.element("div").classes("h-6")

                def _field(label: str, icon_src: str, placeholder: str, *, password: bool = False) -> ui.input:
                    with ui.column().classes("w-full gap-2"):
                        with ui.row().classes("items-center gap-2"):
                            ui.image(icon_src).classes("w-5 h-5")
                            ui.label(label).classes("text-gray-200 text-base")

                        # input wrapper to control background + rounding
                        with ui.element("div").classes("login_input_wrap w-full rounded-xl border border-white/10").style(
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

                    def _do_login() -> None:
                        if on_login:
                            on_login()

                    ui.button("Login", on_click=_do_login) \
                        .props("unelevated") \
                        .classes("w-full rounded-xl py-4 text-lg font-medium") \
                        .style(f"background-color: {theme.accent} !important; color: {theme.primary} !important;")

                    ui.html(
                        f"""
                        <div style="margin-top: 2px; color: {theme.primary}; font-size: 14px;">
                          Forgot your password? <span style="color: {theme.accent};">Register here</span>
                        </div>
                        """.strip(),
                        sanitize=False,
                    )

    return root


