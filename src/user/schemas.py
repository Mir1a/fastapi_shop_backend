from typing import Optional
from fastapi_users import schemas
from pydantic import BaseModel


class UserRead(schemas.BaseUser[int]):
    id: int
    name: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    manager_id: Optional[int] = None

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    name: str
    password: str
    role_id: int
    manager_id: Optional[int] = None


class RoleBase(BaseModel):
    name: str
    can_view_all_requests: Optional[bool] = False
    can_view_own_requests: Optional[bool] = True
    can_manage_users: Optional[bool] = False


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int

    class Config:
        from_attributes = True
