import uuid
from datetime import datetime
from sqlalchemy import TIMESTAMP, Column, text
from sqlalchemy.dialects.postgresql import UUID

class UUIDPkMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

class TimestampMixin:
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    updated_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), onupdate=text("now()"), nullable=False
    )

class SoftDeleteMixin:
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
