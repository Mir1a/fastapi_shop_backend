from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database import get_async_session, async_sessionmaker
from src.product import models, schemas

router = APIRouter(
    prefix="/product",
    tags=["Product"]
)

@router.post("/item_create")
async def add_item(new_item:  Annotated[schemas.ItemCreate, Depends()], session: AsyncSession = Depends(get_async_session)):
    async with session.begin():
        db_item = models.Item(title=new_item.title,
                              description=new_item.description,
                              price=new_item.price,
                              code=new_item.code,
                              color=new_item.color,
                              weight=new_item.weight,
                              height=new_item.height,
                              width=new_item.width,
                              types=new_item.types,
                              amount=new_item.amount)
        session.add(db_item)
    return db_item

@router.get("/items_all")
@cache(expire=30)
async def get_items():
    async with async_sessionmaker() as session:
        query = select(models.Item)
        result = await session.execute(query)
        items = result.scalars().all()
        return items
@router.post("/order_create")
async def create_order(order: Annotated[schemas.OrderCreate, Depends()], session: AsyncSession = Depends(get_async_session)):
    async with session.begin():
        db_order_items = []
        for order_item in order.items:
            db_item = await session.get(models.Item, order_item.item_id)
            if db_item is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Item with id {order_item.item_id} not found")
            db_order_items.append(db_item)

        db_order = models.Order(
            sum_price=order.sum_price,
            amount_items=order.amount_items,
            status=order.status,
            items=db_order_items
        )
        session.add(db_order)
    return db_order

@router.get("/orders_all")
async def get_orders():
    async with async_sessionmaker() as session:
        query = select(models.Order).options(selectinload(models.Order.items))
        result = await session.execute(query)
        orders = result.scalars().all()
        return orders
