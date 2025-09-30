from pydantic import BaseModel
from uuid import UUID
from app.schemas.common import ORMModel

class ExecutorBase(ORMModel):
    name: str
    note: str | None = None

class ExecutorCreate(ExecutorBase):
    pass

class ExecutorUpdate(ORMModel):
    name: str | None = None
    note: str | None = None

class ExecutorOut(ExecutorBase):
    id: UUID
