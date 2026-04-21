from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.profile import router as profile_router
from app.api.user import router as user_router
from app.api.ws import router as ws_router

api_router = APIRouter()

api_router.include_router(auth_router, tags=["auth"])
api_router.include_router(health_router, tags=["health"])
api_router.include_router(profile_router, tags=["profile"])
api_router.include_router(user_router, tags=["user"])
api_router.include_router(ws_router, tags=["ws"])
