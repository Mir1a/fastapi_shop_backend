from sqlalchemy import Column, Integer, String, Float, Enum as sqlenum, ForeignKey, Boolean, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from enum import Enum

Base = declarative_base()

class Types(Enum):
    КБТ = "Крупнобытовая техника"
    МБТ = "Мелкобытовая техника"
    ТВ = "Телевизоры"
    НМ = "New Media"
    Acc = "Аксессуры"

class Order_statuses(Enum):
    Черновик = "Черновик",
    Ожидание_оплаты = 'Ожидание оплаты',
    Оплачен = 'Оплачен',
    В_пути = "В пути",
    Товар_в_пункте_назначения = "Товар в пункте назначения"

class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    code = Column(Integer, nullable=False)
    color = Column(String, nullable=True)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    width = Column(Float, nullable=True)
    type = Column(sqlenum(Types), nullable=True)
    amount = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="favorites")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    avatar = Column(String, nullable=True)
    born = Column(String, nullable=True)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    favorite = relationship("Item", back_populates="user")
    order = relationship("Order", back_populates="user")

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    sum_price = Column(Integer, nullable=False)
    amount_items = Column(Integer, nullable=False)
    status = Column(sqlenum(Order_statuses), nullable=False)
    discount = Column(Integer, nullable=False, default=0)

    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="orders")


# items = models.ManyToManyField(to="product.Item", related_name="orders")
#
# # class Transaction(models.Model):
# #     code = models.CharField(max_length=50)
# #     user = models.ForeignKey(to="midas.User", on_delete=models.CASCADE)
# #     price = models.DecimalField(max_digits=10, decimal_places=2, default="1")
# #     status = models.CharField(max_length=255, choices=choices.statuses)
# #     order = models.OneToOneField(to="product.Order", on_delete=models.CASCADE)
# #     create_at = models.DateTimeField(default=timezone.now)