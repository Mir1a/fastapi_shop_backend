from pydantic import BaseModel
from typing import Optional

from enum import Enum

class item_type(str,Enum):
    KBT = "Крупнобытовая техника"
    MBT = "Мелкобытовая техника"
    TV = "Телевизоры"
    New_Media = "New Media"
    ACC = "Аксессуры"

#region -----Item-----
class ItemBase(BaseModel):
    title: str
    description: Optional[str]
    price: int
    code: int
    color: Optional[str] = None
    weight: Optional[int] = None
    height: Optional[int] = 0
    width: Optional[int] = 0
    types: item_type
    amount: Optional[int] = 0


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    class Config:
        orm_mode = True

#endregion


#region -----Order-----
class OrderBase(BaseModel):
    discount: int


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    sum_price: int
    amount_items: int
    status: str
    user_id: int

    class Config:
        orm_mode = True

#endregion

#region -----User-----