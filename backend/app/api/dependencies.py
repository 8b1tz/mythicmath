from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.engine.database import get_session as get_db_session
from app.errors import unauthorized
from app.services.session_service import get_session as get_auth_session
from app.services.user_service import UserService

user_service = UserService()


async def get_current_user(
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db_session),
):
    if not authorization or not authorization.startswith("Bearer "):
        raise unauthorized(
            code="AUTH_HEADER_INVALID",
            detail="Missing or invalid token",
        )

    token = authorization.split(" ", 1)[1].strip()
    session_data = await get_auth_session(token)
    if not session_data:
        raise unauthorized(
            code="AUTH_TOKEN_INVALID",
            detail="Invalid token",
        )

    user_id = session_data.get("user_id")
    user = await user_service.get_user(db, user_id)
    if not user:
        raise unauthorized(
            code="AUTH_USER_NOT_FOUND",
            detail="User not found",
        )

    return user
