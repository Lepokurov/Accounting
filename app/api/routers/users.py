from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from uuid import UUID
from app.db.session import get_session
from app.api.deps import auth_bearer, get_pagination, Pagination
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(auth_bearer)])

@router.get("/", response_model=list[UserOut])
async def list_users(p: Pagination = Depends(get_pagination), session: AsyncSession = Depends(get_session)):
    q = select(User).where(User.deleted_at.is_(None)).order_by(User.created_at.desc()).offset(p.offset).limit(p.limit)
    rows = (await session.execute(q)).scalars().all()
    return rows

@router.post("/", response_model=UserOut, status_code=201)
async def create_user(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    obj = User(**payload.model_dump())
    session.add(obj)
    await session.flush()
    return obj

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: UUID, session: AsyncSession = Depends(get_session)):
    obj = await session.get(User, user_id)
    if not obj or obj.deleted_at is not None:
        raise HTTPException(404, "User not found")
    return obj

@router.patch("/{user_id}", response_model=UserOut)
async def update_user(user_id: UUID, payload: UserUpdate, session: AsyncSession = Depends(get_session)):
    obj = await session.get(User, user_id)
    if not obj or obj.deleted_at is not None:
        raise HTTPException(404, "User not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await session.flush()
    return obj

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: UUID, session: AsyncSession = Depends(get_session)):
    obj = await session.get(User, user_id)
    if not obj or obj.deleted_at is not None:
        return
    from datetime import datetime, timezone
    obj.deleted_at = datetime.now(tz=timezone.utc)
    await session.flush()
