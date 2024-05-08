from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

from src.product.models import Order

class transaction_type(str,Enum):
    Выполнено = "Выполнено"
    Ожидание_транзакции = "Ожидание транзакции"

class TransactionBase(BaseModel):
    price: int
    status: transaction_type
    user_id: int
    order_id: int

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int

    class Config:
        from_attributes = True
