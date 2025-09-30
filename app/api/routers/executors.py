from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.db.session import get_session
from app.api.deps import auth_bearer, get_pagination, Pagination
from app.models.executor import Executor
from app.schemas.executor import ExecutorCreate, ExecutorOut, ExecutorUpdate

router = APIRouter(prefix="/executors", tags=["Executors"], dependencies=[Depends(auth_bearer)])

@router.get("/", response_model=list[ExecutorOut])
async def list_executors(p: Pagination = Depends(get_pagination), session: AsyncSession = Depends(get_session)):
    q = select(Executor).where(Executor.deleted_at.is_(None)).order_by(Executor.created_at.desc()).offset(p.offset).limit(p.limit)
    rows = (await session.execute(q)).scalars().all()
    return rows

@router.post("/", response_model=ExecutorOut, status_code=201)
async def create_executor(payload: ExecutorCreate, session: AsyncSession = Depends(get_session)):
    obj = Executor(**payload.model_dump())
    session.add(obj)
    await session.flush()
    return obj

@router.get("/{executor_id}", response_model=ExecutorOut)
async def get_executor(executor_id: UUID, session: AsyncSession = Depends(get_session)):
    obj = await session.get(Executor, executor_id)
    if not obj or obj.deleted_at is not None:
        raise HTTPException(404, "Executor not found")
    return obj

@router.patch("/{executor_id}", response_model=ExecutorOut)
async def update_executor(executor_id: UUID, payload: ExecutorUpdate, session: AsyncSession = Depends(get_session)):
    obj = await session.get(Executor, executor_id)
    if not obj or obj.deleted_at is not None:
        raise HTTPException(404, "Executor not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await session.flush()
    return obj

@router.delete("/{executor_id}", status_code=204)
async def delete_executor(executor_id: UUID, session: AsyncSession = Depends(get_session)):
    obj = await session.get(Executor, executor_id)
    if not obj or obj.deleted_at is not None:
        return
    from datetime import datetime, timezone
    obj.deleted_at = datetime.now(tz=timezone.utc)
    await session.flush()