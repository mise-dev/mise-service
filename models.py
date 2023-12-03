from typing import Optional, List, Union
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
    password: str

class Shop(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    name: str
    description: str
    momo: int
    profile_image: str


class Product(SQLModel, table=True):
    id: int = Field(primary_key=True)
    shop_id: Optional[int] = Field(default=None, foreign_key="shop.id")
    name: str
    price: int
    description: str
    images: str
    active: bool
    stock: int
    category: str

class TransactionProductSnapshot(SQLModel):
    product: Product
    quantity: int

class Transaction(SQLModel, table=True):
    id: int = Field(primary_key=True)
    uid: int = Field(default=None, foreign_key="user.id") # id of the user who initiated the transaction
    products: List[TransactionProductSnapshot]
    date: int # utc timestamp
    payment_method: Union["momo", "credit-card"]
    amount_total: int
    status: Union["Pending","Procession", "Complete"]
