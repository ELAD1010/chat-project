"""
Define the authentication logic for the client side.
Register and login (dummy logic for now).
"""


def _is_valid_email(email: str) -> bool:
    email = (email or "").strip()
    if "@" not in email:
        return False
    local, _, domain = email.partition("@")
    return bool(local) and "." in domain and not domain.startswith(".") and not domain.endswith(".")