from datetime import datetime

from sqlalchemy import DateTime, Boolean, Column, ForeignKey, Integer, String, Enum, TIMESTAMP, Table
from sqlalchemy.orm import relationship

from .choices import transaction_statuses
from src.database import Base
from src.user.models import User
from src.product.models import Order


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(Integer, autoincrement=True)
    price = Column(Integer)
    status = Column(Enum(*transaction_statuses, name="transaction_enum"))
    created_at = Column(DateTime, default=datetime.now)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    order_id = Column(Integer, ForeignKey('orders.id'), unique=True)
    order = relationship("Order", back_populates="transaction")
