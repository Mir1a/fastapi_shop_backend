from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database import get_async_session, async_sessionmaker
from src.transaction import models, schemas
from src.product.models import Order

router = APIRouter(
    prefix="/transaction",
    tags=["Transaction"]
)

@router.post("/transaction_create")
async def create_transaction(transaction: Annotated[schemas.TransactionCreate, Depends()], session: AsyncSession = Depends(get_async_session)):
    async with session.begin():
        db_user = await session.get(models.User, transaction.user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail=f"User with id {transaction.user_id} not found")

        db_order = await session.get(models.Order, transaction.order_id)
        if db_order is None:
            raise HTTPException(status_code=404, detail=f"Order with id {transaction.order_id} not found")

        db_transaction = models.Transaction(
            price=transaction.price,
            status=transaction.status,
            user=db_user,
            order=db_order
        )
        session.add(db_transaction)
    return db_transaction