from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Enum
from typing import Optional
from .engine import Base

import enum


class UserType(enum.Enum):
    regular = 0
    admin = 1



class User(Base):
    __tablename__ ="users"

    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column(Enum(UserType))
    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)
    


class Category(Base):
    __tablename__="categories"

    title: Mapped[str] = mapped_column(unique=True)

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)



class Product(Base):
    __tablename__="products"

    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    user: Mapped[str] = mapped_column(ForeignKey("users.username"))


    category: Mapped[str] = mapped_column(ForeignKey("categories.title"))
    on_sale: Mapped[Optional[bool]] = mapped_column(default=False)
    in_stock: Mapped[bool] = mapped_column(default=True)
    on_sale_price: Mapped[Optional[int]] = mapped_column(default=None)

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)


class Image(Base):
    __tablename__ = "images"

    image: Mapped[str] = mapped_column()
    product_title: Mapped[str] = mapped_column(ForeignKey("products.title"))

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)


class Cart(Base):
    __tablename__ = "carts"

    user: Mapped[str] = mapped_column(ForeignKey("users.username"))

    paid: Mapped[bool] = mapped_column(default=False)
    complete: Mapped[bool] = mapped_column(default=False)
    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)



class CartItem(Base):
    __tablename__ = "cartitems"

    product: Mapped[str] = mapped_column(ForeignKey("products.title"))
    cart: Mapped[UUID] = mapped_column(ForeignKey("carts.id"))
    quantity: Mapped[int] = mapped_column()

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)

