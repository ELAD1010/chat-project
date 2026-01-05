from __future__ import annotations

from typing import Callable, Optional

from nicegui import ui

from auth_page import AuthTheme, build_auth_page


def build_login_page(
    *,
    on_login: Optional[Callable[[str, str], dict]] = None,
    on_success: Optional[Callable[[dict], None]] = None,
    on_show_register: Optional[Callable[[], None]] = None,
    theme: AuthTheme = AuthTheme(),
) -> ui.element:
    return build_auth_page(
        title="Welcome Back!",
        subtitle="We missed you!",
        primary_button_text="Login",
        on_primary=on_login,
        on_success=on_success,
        footer_prefix="Forgot your password?",
        footer_action_text="Register here",
        on_footer_action=on_show_register,
        theme=theme,
    )
