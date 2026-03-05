from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class UsersRepo:
    @staticmethod
    async def create_user(db: AsyncSession, data: UserCreate):
        user = User(
            name=data.name,
            email=data.email,
            password=data.password,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def list(db: AsyncSession, limit: int = 50, offset: int = 0) -> list[User]:
        result = await db.execute(select(User).limit(limit).offset(offset))
        return list(result.scalars().all())

    @staticmethod
    async def update(db: AsyncSession, user: User, data: UserUpdate) -> User:
        if data.name is not None:
            user.name = data.name
        if data.email is not None:
            user.email = data.email
        if data.password is not None:
            user.set_password(data.password)

        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_by_id_with_tasks(db: AsyncSession, user_id: int):
        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.tasks))
        )

        result = await db.execute(stmt)
        return result.scalar_one_or_none()