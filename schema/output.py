from uuid import UUID

from pydantic import BaseModel


class UserOutput(BaseModel):
    username: str
    id: UUID
    #role: str


class PostOutput(BaseModel):
    title: str
    user: str
    id: UUID


class CategoryOutput(BaseModel):
    title: str
    id: UUID


class ImageOutput(BaseModel):
    image: str
    product_title: str


class CartItemOutput(BaseModel):
    product: str
    cart: UUID
    quantity: int


class CartOutput(BaseModel):
    user: str
    paid: bool
    complete: bool
    items: list[CartItemOutput]