from uuid import UUID
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from app.models.entry import Entry, EntryStatus

class EntryFilters:
    def __init__(self, user_id: UUID | None = None, executor_id: UUID | None = None, manager_id: UUID | None = None,
                 date_from: date | None = None, date_to: date | None = None, status: EntryStatus | None = None):
        self.user_id = user_id
        self.executor_id = executor_id
        self.manager_id = manager_id
        self.date_from = date_from
        self.date_to = date_to
        self.status = status

    def to_clause(self):
        clauses = [Entry.deleted_at.is_(None)]
        if self.user_id:
            clauses.append(Entry.user_id == self.user_id)
        if self.executor_id:
            clauses.append(Entry.executor_id == self.executor_id)
        if self.manager_id:
            clauses.append(Entry.manager_id == self.manager_id)
        if self.date_from:
            clauses.append(Entry.date >= self.date_from)
        if self.date_to:
            clauses.append(Entry.date <= self.date_to)
        if self.status:
            clauses.append(Entry.status == self.status)
        return and_(*clauses)

