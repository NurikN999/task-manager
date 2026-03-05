from pydantic import BaseModel, EmailStr
from app.schemas.task import TaskShortOut

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = {"from_attributes": True}

class UserOutWithTasks(BaseModel):
    id: int
    name: str
    email: EmailStr
    tasks: list[TaskShortOut] = []

    model_config = {"from_attributes": True}