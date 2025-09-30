from sqlalchemy import Column, ForeignKey, String, Date, Numeric, CheckConstraint, Enum, Index
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.mixins import UUIDPkMixin, TimestampMixin, SoftDeleteMixin
import enum

class EntryStatus(enum.Enum):
    draft = "draft"
    pending = "pending"
    approved = "approved"
    paid = "paid"
    cancelled = "cancelled"
    rejected = "rejected"

class Entry(Base, UUIDPkMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "entries"

    user_id = Column("user_id", ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    executor_id = Column("executor_id", ForeignKey("executors.id", ondelete="RESTRICT"), nullable=False, index=True)
    manager_id = Column("manager_id", ForeignKey("managers.id", ondelete="RESTRICT"), nullable=False, index=True)

    date = Column(Date, nullable=False, index=True)
    currency = Column(String(3), nullable=False, index=True)
    amount = Column(Numeric(18, 2), nullable=False)
    status = Column(Enum(EntryStatus, name="entry_status"), nullable=False, index=True, default=EntryStatus.draft)

    __table_args__ = (
        CheckConstraint("amount >= 0", name="ck_entries_amount_nonnegative"),
        CheckConstraint("char_length(currency) = 3", name="ck_entries_currency_iso_len"),
        Index("ix_entries_sort", "date", "id"),
    )

    user = relationship("User")
    executor = relationship("Executor")
    manager = relationship("Manager")
