from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.engine.database import get_session
from app.schemas.user import (
    UserLoginRequest,
    UserLogoutRequest,
    UserLogoutResponse,
    UserRegisterRequest,
    UserRegisterResponse,
)
from app.services.user_service import UserService
from app.services.session_service import create_session, revoke_session

router = APIRouter()
user_service = UserService()


def _clean_str(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


@router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserRegisterRequest,
    session: AsyncSession = Depends(get_session),
):
    email = payload.email.strip().lower()
    name = payload.name.strip()
    existing = await user_service.get_user_by_email(session, email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    existing_name = await user_service.get_user_by_name(session, name)
    if existing_name:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Name already registered")

    user = await user_service.create_user(
        session=session,
        name=name,
        email=email,
        password=payload.password,
    )

    token = await create_session(user_id=user.id, email=user.email)

    return UserRegisterResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        token=token,
    )


@router.post("/login", response_model=UserRegisterResponse)
async def login_user(
    payload: UserLoginRequest,
    session: AsyncSession = Depends(get_session),
):
    identifier = _clean_str(payload.identifier)
    if not identifier:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Identifier is required",
        )

    if "@" in identifier:
        user = await user_service.get_user_by_email(session, identifier.lower())
    else:
        user = await user_service.get_user_by_name(session, identifier)

    if not user or not user_service.verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = await create_session(user_id=user.id, email=user.email)
    return UserRegisterResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        token=token,
    )


@router.post("/logout", response_model=UserLogoutResponse)
async def logout_user(payload: UserLogoutRequest):
    await revoke_session(payload.token)
    return UserLogoutResponse(success=True)
