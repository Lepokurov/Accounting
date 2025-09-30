from decimal import Decimal
from uuid import UUID
from datetime import date
from pydantic import BaseModel, Field
from app.schemas.common import ORMModel
from app.models.entry import EntryStatus

class EntryBase(ORMModel):
    user_id: UUID
    executor_id: UUID
    manager_id: UUID
    date: date
    currency: str = Field(min_length=3, max_length=3, examples=["RSD", "EUR"])
    amount: Decimal
    status: EntryStatus

class EntryCreate(EntryBase):
    pass

class EntryUpdate(ORMModel):
    user_id: UUID | None = None
    executor_id: UUID | None = None
    manager_id: UUID | None = None
    date: date | None = None
    currency: str | None = None
    amount: Decimal | None = None
    status: EntryStatus | None = None

class EntryOut(EntryBase):
    id: UUID