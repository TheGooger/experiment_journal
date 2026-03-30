from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])

service = AuthService()

@router.post("/register", response_model=UserRead)
async def register(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await service.register(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.post("/login")
async def login(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        token = await service.login(db, data.user_name, data.pasword)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    