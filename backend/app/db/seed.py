import asyncio

from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import select

from app.engine.database import AsyncSessionLocal
from app.models.user import User
from app.services.security import hash_password


async def seed() -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.email == "seed@local"))
        existing = result.scalar_one_or_none()
        if existing:
            return

        session.add(
            User(
                name="Seed User",
                email="seed@local",
                password_hash=hash_password("seed123"),
                photo_url=None,
                xp=0,
                level=1,
                total_score=0,
                ranked_wins=0,
            )
        )
        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
