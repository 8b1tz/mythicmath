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

    async def get_by_username(self, session: AsyncSession, username: str) -> Optional[User]:
        result = await session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def create(
        self,
        session: AsyncSession,
        username: str,
        email: str,
        password_hash: str,
        photo_url: Optional[str] = None,
    ) -> User:
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            photo_url=photo_url,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def update(
        self,
        session: AsyncSession,
        user: User,
        email: Optional[str] = None,
        password_hash: Optional[str] = None,
    ) -> User:
        if email is not None:
            user.email = email
        if password_hash is not None:
            user.password_hash = password_hash
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
