from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.product import models, schemas

router = APIRouter(
    prefix="/item",
    tags=["Product"]
)

@router.post("/")
async def add_item(new_item:  Annotated[schemas.ItemCreate, Depends()], session: AsyncSession = Depends(get_async_session)):
    async with session.begin():
        db_item = models.Item(title=new_item.title, description=new_item.description, price=new_item.price, code=new_item.code, color=new_item.color, weight=new_item.weight, height=new_item.height, width=new_item.width, types=new_item.types, amount=new_item.amount)
        session.add(db_item)
    return db_item
