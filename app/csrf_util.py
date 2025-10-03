from fastapi import Request
import secrets


def generate_csrf_token() -> str:
    return secrets.token_urlsafe(32)

def validate_csrf_token(request: Request, token: str) -> bool:
    session_token = request.session.get("csrf_token")
    if not session_token or session_token != token:
        return False
    return True
