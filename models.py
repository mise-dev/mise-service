from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    email: str
    contact_phone: int
    momo: int
    profile_image: str
    location: str
    date_of_birth: str
    active: bool

class Shop(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="User.id")
    name: str
    description: str
    momo: int
    profile_image: str


class Product(SQLModel, table=True):
    id: int = Field(primary_key=True)
    shop_id: Optional[int] = Field(default=None, foreign_key="Shop.id")
    name: str
    price: int
    description: str
    images: str
    active: bool
    stock: int
    category: str
