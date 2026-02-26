from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.repositories.UsersRepo import UsersRepo
from app.schemas.user import UserCreate, UserUpdate, UserOut

router = APIRouter(prefix="/users", tags=["Пользователи"], dependencies=[Depends(get_current_user)])

@router.get("/", response_model=list[UserOut], status_code=status.HTTP_200_OK)
async def list_users(
        limit: int = 50,
        offset: int = 0,
        db: AsyncSession = Depends(get_db)
):
    return await UsersRepo.list(db, limit, offset)

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
        payload: UserCreate,
        db: AsyncSession = Depends(get_db),
):
    existing = await UsersRepo.get_by_email(db, email=payload.email)
    if existing:
        raise HTTPException(status_code=409, detail="email уже занят")
    return await UsersRepo.create_user(db, payload)