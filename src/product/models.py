from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, TIMESTAMP, Table
from sqlalchemy.orm import relationship

from src.database import Base
from .choices import item_type

order_items = Table('order_items', Base.metadata,
                    Column('order_id', Integer, ForeignKey('orders.id')),
                    Column('item_id', Integer, ForeignKey('items.id'))
                    )


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, nullable=True)
    price = Column(Integer)
    code = Column(Integer)
    color = Column(String, nullable=True)
    weight = Column(Integer, nullable=True)
    height = Column(Integer, default=0)
    width = Column(Integer, default=0)
    types = Column(Enum(*item_type, name="item_type_enum"))
    amount = Column(Integer, default=0)

    orders = relationship("Order", secondary=order_items, back_populates="items")


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)

    items = relationship("Item", secondary=order_items, back_populates="orders")

