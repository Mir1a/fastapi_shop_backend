from pydantic import BaseModel
from typing import List, Optional

from enum import Enum

#region -----Item-----

class order_statuses(str,Enum):
    Черновик="Черновик",
    Ожидание_оплаты="Ожидание оплаты",
    Оплачен="Оплачен",
    В_пути="В пути",
    Товар_в_пункте_назначения="Товар в пункте назначения"


class item_type(str,Enum):
    KBT = "Крупнобытовая техника"
    MBT = "Мелкобытовая техника"
    TV = "Телевизоры"
    New_Media = "New Media"
    ACC = "Аксессуры"


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
        from_attributes = True

#endregion


#region -----Order-----



class OrderItem(BaseModel):
    item_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItem]
    sum_price: int
    amount_items: int
    status: order_statuses

class Order(BaseModel):
    items: List[OrderItem]

    class Config:
        orm_mode = True

#endregion