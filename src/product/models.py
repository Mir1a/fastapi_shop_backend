from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, TIMESTAMP
from sqlalchemy.orm import relationship

from src.database import Base
from .choices import item_type

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    price = Column(Integer)
    code = Column(Integer, unique=True)
    color = Column(String)
    weight = Column(Integer)
    height = Column(Integer)
    width = Column(Integer)
    types = Column(Enum(*item_type, name="item_type_enum"))
    amount = Column(Integer)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    sum_price = Column(Integer)
    amount_items = Column(Integer)
    status = Column(String)
    discount = Column(Integer)
    #items = Column()

    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="orders")

