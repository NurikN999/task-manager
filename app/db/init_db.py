from app.db.session import engine
from app.db.base import Base

from app.models.user import User
from app.models.task import Task

async def init_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)