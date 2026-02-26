from typing import AsyncGenerator
from jose import jwt, JWTError

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import SessionLocal
from app.repositories.UsersRepo import UsersRepo

from app.core.security import ALGORITHM
from app.core.config import settings

security_scheme = HTTPBearer()

# Данный метод отвечает за создание сессии с базой данных
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# Этот метод отвечает за авторизацию пользователей
async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
        db: AsyncSession = Depends(get_db),
):
    """
    1) Берем токен из заголовка Authorization: Bearer <token>
    2) Декодируем токен
    3) Достаем user_id из sub
    4) Ищем пользователя в БД
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        subject = payload["sub"]
        if subject is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user_id = int(subject)
    except (JWTError, ValueError) as e:
        # Debug: include actual error to diagnose (remove in production)
        raise HTTPException(status_code=401, detail=f"Invalid credentials: {type(e).__name__}: {e}")

    user = await UsersRepo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
