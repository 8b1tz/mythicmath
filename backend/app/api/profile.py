from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.engine.database import get_session as get_db_session
from app.error_codes import ErrorCode
from app.errors import bad_request
from app.schemas.user import (
    UserAvatarPresetRequest,
    UserAvatarResponse,
    UserProfileResponse,
)
from app.services.avatar_presets import build_avatar_preset_value, is_valid_avatar_preset

router = APIRouter()


def calculate_xp_to_next_level(level: int) -> int:
    return (level + 1) * 100


@router.get("/profile", response_model=UserProfileResponse)
async def get_profile(current_user=Depends(get_current_user)):
    xp_to_next_level = calculate_xp_to_next_level(current_user.level)

    return UserProfileResponse(
        userId=current_user.id,
        username=current_user.username,
        email=current_user.email,
        image=current_user.photo_url,
        day_learning_streak=0,
        ranked_victories=current_user.ranked_wins,
        xpCurrent=current_user.xp,
        xpToNextLevel=xp_to_next_level,
        level=current_user.level,
    )


@router.put("/avatar/preset", response_model=UserAvatarResponse)
async def update_avatar_preset(
    payload: UserAvatarPresetRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    avatar_id = payload.avatar_id.strip()
    if not avatar_id or not is_valid_avatar_preset(avatar_id):
        raise bad_request(
            code=ErrorCode.INVALID_AVATAR_PRESET,
            detail="Invalid avatar preset",
        )

    image_value = build_avatar_preset_value(avatar_id)
    current_user.photo_url = image_value
    await db.commit()
    await db.refresh(current_user)

    return UserAvatarResponse(result=True, image=image_value)
