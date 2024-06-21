from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table, DateTime
from sqlalchemy.orm import relationship
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from ..database import Base

user_items = Table('user_items', Base.metadata,
                   Column('item_id', Integer, ForeignKey('items.id')),
                   Column('user_id', Integer, ForeignKey('users.id')))


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="role")


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    name = Column(String)
    last_name = Column(String, nullable=True)
    avatar = Column(String, nullable=True)
    born = Column(DateTime, nullable=True)
    hashed_password = Column(String(length=1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'))
    manager_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    role = relationship("Role", back_populates="users")
    manager = relationship("User", remote_side=[id], backref="subordinates")
    items = relationship("Item", secondary=user_items, back_populates="users")
