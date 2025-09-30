from pydantic import BaseModel
from uuid import UUID
from app.schemas.common import ORMModel

class UserBase(ORMModel):
    name: str
    note: str | None = None

class UserCreate(UserBase):
    pass

class UserUpdate(ORMModel):
    name: str | None = None
    note: str | None = None

class UserOut(UserBase):
    id: UUID

