from decimal import Decimal
from pydantic import BaseModel, field_serializer
from uuid import UUID
from datetime import datetime, date

class ORMModel(BaseModel):
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "use_enum_values": True,
    }

class DecimalAsStr(BaseModel):
    @field_serializer("amount")
    def serialize_decimal(cls, v: Decimal):
        return f"{v:.2f}" if v is not None else None
