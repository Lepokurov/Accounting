from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.db.session import get_session
from app.api.deps import auth_bearer, get_pagination, Pagination
from app.models.manager import Manager
from app.schemas.manager import ManagerCreate, ManagerOut, ManagerUpdate

router = APIRouter(prefix="/managers", tags=["Managers"], dependencies=[Depends(auth_bearer)])

@router.get("/", response_model=list[ManagerOut])
async def list_managers(p: Pagination = Depends(get_pagination), session: AsyncSession = Depends(get_session)):
    q = select(Manager).where(Manager.deleted_at.is_(None)).order_by(Manager.created_at.desc()).offset(p.offset).limit(p.limit)
    rows = (await session.execute(q)).scalars().all()
    return rows

@router.post("/", response_model=ManagerOut, status_code=201)
async def create_manager(payload: ManagerCreate, session: AsyncSession = Depends(get_session)):
    obj = Manager(**payload.model_dump())
    session.add(obj)
    await session.flush()
    return obj

@router.get("/{manager_id}", response_model=ManagerOut)
async def get_manager(manager_id: UUID, session: AsyncSession = Depends(get_session)):
    obj = await session.get(Manager, manager_id)
    if not obj or obj.deleted_at is not None:
        raise HTTPException(404, "Manager not found")
    return obj

@router.patch("/{manager_id}", response_model=ManagerOut)
async def update_manager(manager_id: UUID, payload: ManagerUpdate, session: AsyncSession = Depends(get_session)):
    obj = await session.get(Manager, manager_id)
    if not obj or obj.deleted_at is not None:
        raise HTTPException(404, "Manager not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await session.flush()
    return obj

@router.delete("/{manager_id}", status_code=204)
async def delete_manager(manager_id: UUID, session: AsyncSession = Depends(get_session)):
    obj = await session.get(Manager, manager_id)
    if not obj or obj.deleted_at is not None:
        return
    from datetime import datetime, timezone
    obj.deleted_at = datetime.now(tz=timezone.utc)
    await session.flush()
