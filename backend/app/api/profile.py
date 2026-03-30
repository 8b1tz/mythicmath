import mimetypes
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Header, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.engine.database import get_session as get_db_session
from app.schemas.user import UserAvatarResponse, UserProfileResponse
from app.services.session_service import get_session as get_auth_session
from app.services.user_service import UserService

router = APIRouter()
user_service = UserService()

BASE_DIR = Path(__file__).resolve().parents[2]
AVATAR_DIR = BASE_DIR / "uploads" / "avatars"
AVATAR_DIR.mkdir(parents=True, exist_ok=True)


async def get_current_user(
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db_session),
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid token",
        )

    token = authorization.split(" ", 1)[1].strip()
    session_data = await get_auth_session(token)
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user_id = session_data.get("user_id")
    user = await user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


def calculate_xp_to_next_level(level: int) -> int:
    return (level + 1) * 100


@router.get("/profile", response_model=UserProfileResponse)
async def get_profile(current_user=Depends(get_current_user)):
    xp_to_next_level = calculate_xp_to_next_level(current_user.level)

    return UserProfileResponse(
        userId=current_user.id,
        name=current_user.name,
        image=current_user.photo_url,
        day_learning_streak=0,
        ranked_victories=current_user.ranked_wins,
        xpCurrent=current_user.xp,
        xpToNextLevel=xp_to_next_level,
        level=current_user.level,
    )


@router.put("/avatar", response_model=UserAvatarResponse)
async def update_avatar(
    image: UploadFile = File(...),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image type",
        )

    ext = Path(image.filename or "").suffix.lower()
    if not ext:
        ext = mimetypes.guess_extension(image.content_type) or ""

    filename = f"user_{current_user.id}_{uuid4().hex}{ext}"
    file_path = AVATAR_DIR / filename

    contents = await image.read()
    file_path.write_bytes(contents)

    image_url = f"/uploads/avatars/{filename}"
    current_user.photo_url = image_url
    await db.commit()
    await db.refresh(current_user)

    return UserAvatarResponse(result=True, image=image_url)
