from pydantic import BaseModel
from fastapi import UploadFile, File, Body
from typing import Optional, List
from db.models import UserType
from uuid import UUID

class RegisterInput(BaseModel):
    username: str
    password: str
    role: UserType = UserType.regular


class UserInput(BaseModel):
    username: str
    password: str


class UpdateUserProfileInput(BaseModel):
    old_password: str
    new_password: str


class ProductInput(BaseModel):
    title: str
    description: str
    price: int
    category: str
    in_stock: bool = True


#class ImageInput(BaseModel):
  #  image: UploadFile = File()
   # product_title: str


class ImageInput:
    def __init__(self, product_title:str = Body(), file: UploadFile = File()):
        self.product_title = product_title
        self.file = file


class ImageUpdateInput:
    def __init__(self, image_id:UUID = Body(), file: UploadFile = File()):
        self.image_id = image_id
        self.file = file



class Role(BaseModel):
    normal: bool = True
    admin: bool = False


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    #on_sale: Optional[bool] = None
    #in_stock: Optional[bool] = None
    #on_sale_price: Optional[int] = None