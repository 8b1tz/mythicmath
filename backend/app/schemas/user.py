from typing import Optional

from pydantic import BaseModel


class UserRegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class UserRegisterResponse(BaseModel):
    id: int
    name: str
    email: str
    token: str


class UserLoginRequest(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    password: str


class UserProfileResponse(BaseModel):
    userId: int
    name: str
    image: Optional[str] = None
    day_learning_streak: int
    ranked_victories: int
    xpCurrent: int
    xpToNextLevel: int
    level: int


class UserAvatarResponse(BaseModel):
    result: bool
    image: Optional[str] = None
