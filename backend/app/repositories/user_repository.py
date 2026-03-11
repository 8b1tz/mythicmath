from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    async def get_by_id(self, session: AsyncSession, user_id: int) -> Optional[User]:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(
        self, session: AsyncSession, email: str
    ) -> Optional[User]:
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_name(self, session: AsyncSession, name: str) -> Optional[User]:
        result = await session.execute(select(User).where(User.name == name))
        return result.scalar_one_or_none()

    async def create(
        self,
        session: AsyncSession,
        name: str,
        email: str,
        password_hash: str,
        photo_url: Optional[str] = None,
    ) -> User:
        user = User(
            name=name,
            email=email,
            password_hash=password_hash,
            photo_url=photo_url,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
