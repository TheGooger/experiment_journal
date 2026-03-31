from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password, create_access_token


class AuthService:

    def __init__(self) -> None:
        self.repo = UserRepository()

    async def register(self, db: AsyncSession, data: UserCreate):
        existing = await self.repo.get_by_name(db, data.user_name)

        if existing:
            raise ValueError("User already exists")
        
        hashed = hash_password(data.password)

        user = await self.repo.create(db, data.user_name, hashed)

        return user
    
    async def login(self, db: AsyncSession, user_name: str, password: str):
        user = await self.repo.get_by_name(db, user_name)

        if not user:
            raise ValueError("Invalid credentials")
        
        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        
        token = create_access_token({"sub": str(user.id)})

        return token
    