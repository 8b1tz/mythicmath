from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.engine.database import get_session
from app.schemas.user import UserRegisterRequest, UserRegisterResponse
from app.services.user_service import UserService
from app.services.session_service import create_session

router = APIRouter()
user_service = UserService()


@router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserRegisterRequest,
    session: AsyncSession = Depends(get_session),
):
    email = payload.email.strip().lower()
    existing = await user_service.get_user_by_email(session, email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = await user_service.create_user(
        session=session,
        name=payload.name.strip(),
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
