from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from datetime import date
from decimal import Decimal
from app.db.session import get_session
from app.api.deps import auth_bearer, get_pagination, Pagination
from app.models.entry import Entry, EntryStatus
from app.schemas.entry import EntryCreate, EntryOut, EntryUpdate
from app.services.entry_service import EntryFilters

router = APIRouter(prefix="/entries", tags=["Entries"], dependencies=[Depends(auth_bearer)])

@router.get("/", response_model=list[EntryOut])
async def list_entries(
    p: Pagination = Depends(get_pagination),
    session: AsyncSession = Depends(get_session),
    user_id: UUID | None = None,
    executor_id: UUID | None = None,
    manager_id: UUID | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    status: EntryStatus | None = Query(default=None),
):
    filters = EntryFilters(user_id, executor_id, manager_id, date_from, date_to, status)
    q = (
        select(Entry)
        .where(filters.to_clause())
        .order_by(Entry.date.desc(), Entry.id.desc())
        .offset(p.offset)
        .limit(p.limit)
    )
    rows = (await session.execute(q)).scalars().all()
    return rows

@router.post("/", response_model=EntryOut, status_code=201)
async def create_entry(payload: EntryCreate, session: AsyncSession = Depends(get_session)):
    # rely on FK constraints to ensure related exist; optional extra checks could query first
    obj = Entry(**payload.model_dump())
    session.add(obj)
    await session.flush()
    return obj

@router.get("/{entry_id}", response_model=EntryOut)
async def get_entry(entry_id: UUID, session: AsyncSession = Depends(get_session)):
    obj = await session.get(Entry, entry_id)
    if not obj or obj.deleted_at is not None:
        raise HTTPException(404, "Entry not found")
    return obj

@router.patch("/{entry_id}", response_model=EntryOut)
async def update_entry(entry_id: UUID, payload: EntryUpdate, session: AsyncSession = Depends(get_session)):
    obj = await session.get(Entry, entry_id)
    if not obj or obj.deleted_at is not None:
        raise HTTPException(404, "Entry not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await session.flush()
    return obj

@router.delete("/{entry_id}", status_code=204)
async def delete_entry(entry_id: UUID, session: AsyncSession = Depends(get_session)):
    obj = await session.get(Entry, entry_id)
    if not obj or obj.deleted_at is not None:
        return
    from datetime import datetime, timezone
    obj.deleted_at = datetime.now(tz=timezone.utc)
    await session.flush()