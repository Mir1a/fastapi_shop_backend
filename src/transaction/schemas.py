from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

from src.product.models import Order

class TransactionBase(BaseModel):
    code: int
    price: int
    status: str
    created_at: Optional[datetime] = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    order: Order

    class Config:
        orm_mode = True
