from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str
    name: str
    last_name: str
    avatar: Optional[str] = None
    born: Optional[datetime] = None
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
