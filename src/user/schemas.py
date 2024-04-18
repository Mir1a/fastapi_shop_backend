from pydantic import BaseModel

from src.product.schemas import Order


class UserBase(BaseModel):
    email: str
    name: str
    last_name: str
    avatar: str
    born: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_staff: bool
    is_active: bool
    orders: list[Order] = []

    class Config:
        orm_mode = True

#endregion