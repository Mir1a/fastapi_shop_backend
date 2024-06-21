from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List

from sqlalchemy.orm import selectinload

from src.user import schemas, models
from src.database import get_async_session, async_sessionmaker
from src.user.models import Role, User
from src.user.schemas import RoleCreate, Role as RoleSchema, UserCreate, UserRead as UserSchema
from passlib.context import CryptContext
from .base_config import current_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/create_role", response_model=RoleSchema)
async def create_role(role: Annotated[RoleCreate, Depends()], db: AsyncSession = Depends(get_async_session)):
    db_role = Role(**role.dict())
    db.add(db_role)
    await db.commit()
    await db.refresh(db_role)
    return db_role


@router.get("/roles", response_model=List[RoleSchema])
async def get_roles(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Role))
    return result.scalars().all()

@router.post("/create_user", response_model=UserSchema)
async def create_user(user: Annotated[UserCreate, Depends()], db: AsyncSession = Depends(get_async_session)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        email=user.email,
        name=user.name,
        role_id=user.role_id,
        hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user



@router.get("/users_all")
async def get_items():
    async with async_sessionmaker() as session:
        query = select(models.User).options(selectinload(models.User.items))
        result = await session.execute(query)
        items = result.scalars().all()
        return items
