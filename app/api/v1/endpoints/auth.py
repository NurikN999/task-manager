from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.repositories.UsersRepo import UsersRepo
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.schemas.user import UserCreate

router = APIRouter(prefix="/auth", tags=["Авторизация"])

@router.post("/register", status_code=201)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing = await UsersRepo.get_by_email(db, email=payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    password_hash = hash_password(payload.password)
    user = await UsersRepo.create_user(
        db=db,
        data=UserCreate(
            name=payload.name,
            email=payload.email,
            password=password_hash
        )
    )

    return {"id": user.id}

@router.post("/login", status_code=200, response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await UsersRepo.get_by_email(db, email=payload.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)