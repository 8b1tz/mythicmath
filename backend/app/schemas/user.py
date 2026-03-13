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
    identifier: str
    password: str


class UserLogoutRequest(BaseModel):
    token: str


class UserLogoutResponse(BaseModel):
    success: bool
