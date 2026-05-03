from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.engine.database import get_session as get_db_session
from app.errors import conflict, forbidden, unprocessable_entity
from app.schemas.user import UserUpdateRequest, UserUpdateResponse
from app.services.user_service import UserService
from app.services.validation import is_valid_email

router = APIRouter()
user_service = UserService()


def _clean_str(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


@router.patch("/users/{id}", response_model=UserUpdateResponse)
async def update_user(
    id: int,
    payload: UserUpdateRequest,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    if current_user.id != id:
        raise forbidden(
            code="ACCOUNT_UPDATE_FORBIDDEN",
            detail="You can only update your own account",
        )

    user = current_user

    password = _clean_str(payload.password)
    if payload.password is not None and password is None:
        raise unprocessable_entity(
            code="PASSWORD_REQUIRED",
            detail="Password is required",
        )

    email = _clean_str(payload.email)
    if payload.email is not None and email is None:
        raise unprocessable_entity(
            code="EMAIL_REQUIRED",
            detail="Email is required",
        )

    if email is not None:
        if not is_valid_email(email):
            raise unprocessable_entity(
                code="INVALID_EMAIL_FORMAT",
                detail="Invalid email format",
            )

        email = email.lower()
        existing = await user_service.get_user_by_email(session, email)
        if existing and existing.id != id:
            raise conflict(
                code="EMAIL_ALREADY_REGISTERED",
                detail="Email already registered",
            )

    if email is None and password is None:
        raise unprocessable_entity(
            code="EMAIL_OR_PASSWORD_REQUIRED",
            detail="Email or password is required",
        )

    current_password = _clean_str(payload.current_password)
    if current_password is None:
        raise unprocessable_entity(
            code="CURRENT_PASSWORD_REQUIRED",
            detail="Current password is required",
        )

    if not user_service.verify_password(current_password, user.password_hash):
        raise unprocessable_entity(
            code="CURRENT_PASSWORD_INCORRECT",
            detail="Current password is incorrect",
        )

    updated = await user_service.update_user(
        session,
        user=user,
        email=email,
        password=password,
    )

    return UserUpdateResponse(
        id=updated.id,
        username=updated.username,
        email=updated.email,
        xp=updated.xp,
        level=updated.level,
        total_score=updated.total_score,
        ranked_wins=updated.ranked_wins,
        created_at=updated.created_at,
    )
