from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.engine.database import get_session as get_db_session
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
    session: AsyncSession = Depends(get_db_session),
):
    user = await user_service.get_user(session, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    password = _clean_str(payload.password)
    if payload.password is not None and password is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password is required",
        )

    email = _clean_str(payload.email)
    if payload.email is not None and email is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Email is required",
        )

    if email is not None:
        if not is_valid_email(email):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid email format",
            )

        email = email.lower()
        existing = await user_service.get_user_by_email(session, email)
        if existing and existing.id != id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

    if email is None and password is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Email or password is required",
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
