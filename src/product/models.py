from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Table
from sqlalchemy.orm import relationship

from src.database import Base
from .choices import item_type, order_statuses

order_items = Table('order_items', Base.metadata,
                    Column('order_id', Integer, ForeignKey('orders.id')),
                    Column('item_id', Integer, ForeignKey('items.id'))
                    )


supply_sender_items = Table("supply_sender_items", Base.metadata,
                            Column("item_id",Integer, ForeignKey("items.id")),
                            Column("supply_sender",Integer, ForeignKey("supply_senders.id")))

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
    supply_senders = relationship("supply_senders", secondary=supply_sender_items, back_populates="items")


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    sum_price = Column(Integer)
    amount_items = Column(Integer)
    status = Column(Enum(*order_statuses, name="status_enum"))
    discount = Column(Integer)

    items = relationship("Item", secondary=order_items, back_populates="orders")
    transactions = relationship("Transaction", back_populates="order", uselist=False)

class Supply(Base):
    __tablename__ = "supplies"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(String) #сюда вставить ссылку на файл


class Supply_sender(Base):
    __tablename__ = "supply_senders"

    id = Column(Integer, primary_key=True, index=True)
    items = relationship("Item", secondary=supply_sender_items, back_populates="supply_senders")
    amount = Column(Integer)