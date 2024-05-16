from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List

from sqlalchemy.orm import selectinload

from src.user import schemas, models
from src.database import get_async_session, async_sessionmaker


router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.post("/user_create")
async def create_user(user: Annotated[schemas.UserCreate, Depends()], session: AsyncSession = Depends(get_async_session)):
    async with session.begin():
        db_user = models.User(
            email=user.email,
            name=user.name,
            last_name=user.last_name,
            avatar=user.avatar,
            born=user.born,
            is_staff=user.is_staff,
            is_active=user.is_active,
            password=user.password
        )

        session.add(db_user)
    return db_user

@router.get("/users_all")
async def get_items():
    async with async_sessionmaker() as session:
        query = select(models.User).options(selectinload(models.User.items))
        result = await session.execute(query)
        items = result.scalars().all()
        return items
