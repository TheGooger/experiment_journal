from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.user import User


class UserRepository:

    async def get_by_name(self, db: AsyncSession, user_name: str) -> User | None:
        result = await db.execute(
            select(User).where(User.user_name == user_name)
        )
        return result.scalar_one_or_none()
    
    async def create(self, db: AsyncSession, user_name: str, hashed_password: str) -> User:
        user = User(
            user_name=user_name,
            hashed_password=hashed_password,
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user
    