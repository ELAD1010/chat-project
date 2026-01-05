from __future__ import annotations

from typing import Callable, Optional

from nicegui import ui

from auth_page import AuthTheme, build_auth_page


def build_register_page(
    *,
    on_register: Optional[Callable[[str, str], dict]] = None,
    on_success: Optional[Callable[[dict], None]] = None,
    on_show_login: Optional[Callable[[], None]] = None,
    theme: AuthTheme = AuthTheme(),
) -> ui.element:
    return build_auth_page(
        title="Register",
        subtitle="Meet new people and share funny memes.",
        primary_button_text="Register",
        on_primary=on_register,
        on_success=on_success,
        footer_prefix="Already have an account?",
        footer_action_text="Login here!",
        on_footer_action=on_show_login,
        theme=theme,
    )


