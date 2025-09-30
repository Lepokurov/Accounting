from pydantic import BaseModel
from uuid import UUID
from app.schemas.common import ORMModel

class ManagerBase(ORMModel):
    name: str
    note: str | None = None

class ManagerCreate(ManagerBase):
    pass

class ManagerUpdate(ORMModel):
    name: str | None = None
    note: str | None = None

class ManagerOut(ManagerBase):
    id: UUID
