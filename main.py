from fastapi import FastAPI
from app.db.init_db import init_models
from app.db.session import engine
from contextlib import asynccontextmanager
from app.api.v1.router import router as v1_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield
    await engine.dispose()

app = FastAPI(title="Task Manager API", lifespan=lifespan)
app.include_router(v1_router)