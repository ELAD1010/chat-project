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


def login(email: str, password: str) -> dict:
    email = (email or "").strip()
    password = password or ""

    # Dummy logic: require a plausible email and a non-trivial password
    if not _is_valid_email(email):
        return {"status": "error", "message": "Please enter a valid email."}
    if len(password) < 4:
        return {"status": "error", "message": "Password must be at least 4 characters."}

    print("Login successful")
    return {"status": "success", "message": "Login successful", "user_id": email}


def register(email: str, password: str) -> dict:
    email = (email or "").strip()
    password = password or ""

    # Dummy logic: same basic validation; later you can add server calls/uniqueness checks
    if not _is_valid_email(email):
        return {"status": "error", "message": "Please enter a valid email."}
    if len(password) < 4:
        return {"status": "error", "message": "Password must be at least 4 characters."}

    print("Register successful")
    return {"status": "success", "message": "Register successful", "user_id": email}
