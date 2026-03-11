import os
import time
from typing import Any, Dict, Optional, Tuple

from app.services.security import generate_token

SESSION_TTL_SECONDS = int(os.getenv("SESSION_TTL_SECONDS", "86400"))

_memory_sessions: Dict[str, Tuple[Dict[str, Any], float]] = {}


def _cleanup_expired() -> None:
    now = time.time()
    expired = [token for token, (_, exp) in _memory_sessions.items() if exp <= now]
    for token in expired:
        _memory_sessions.pop(token, None)


async def create_session(user_id: int, email: str) -> str:
    token = generate_token()
    payload = {"user_id": user_id, "email": email}

    _cleanup_expired()
    _memory_sessions[token] = (payload, time.time() + SESSION_TTL_SECONDS)
    return token


async def get_session(token: str) -> Optional[Dict[str, Any]]:
    _cleanup_expired()
    entry = _memory_sessions.get(token)
    if not entry:
        return None
    return entry[0]


async def revoke_session(token: str) -> None:
    _memory_sessions.pop(token, None)
