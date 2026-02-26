from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str | None
    deadline: datetime | None
    status: str
    user_id: int

class TaskUpdate(BaseModel):
    title: str | None
    description: str | None
    deadline: datetime | None
    status: str | None

class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None
    deadline: datetime | None
    status: str
    user_id: int

    model_config = {"from_attributes": True}