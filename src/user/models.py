from sqlalchemy import DateTime, Boolean, Column, ForeignKey, Integer, String, Enum, TIMESTAMP, Table
from sqlalchemy.orm import relationship
from src.database import Base

user_items = Table('user_items', Base.metadata,
    Column('item_id', Integer, ForeignKey('items.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    name = Column(String)
    last_name = Column(String)
    avatar = Column(String)
    born = Column(DateTime)
    is_staff = Column(Boolean)
    is_active = Column(Boolean)
    password = Column(String)

    items = relationship("Item", secondary=user_items, back_populates="users")
