from sqlalchemy import Column, String, Text
from app.db.base import Base
from app.models.mixins import UUIDPkMixin, TimestampMixin, SoftDeleteMixin

class User(Base, UUIDPkMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    name = Column(String(200), nullable=False, index=True)
    note = Column(Text, nullable=True)
