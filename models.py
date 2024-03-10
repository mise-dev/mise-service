from typing import Optional, List, Union
from sqlmodel import Field, SQLModel, create_engine, select
from pydantic import BaseModel

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    contact_phone: int
    momo: int
    profile_image: str
    location: str
    date_of_birth: str
    active: bool = Field(default=True)
    password: str

class Shop(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    name: str
    description: str
    momo: int
    profile_image: str


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    shop_id: int = Field(default=None, foreign_key="shop.id")
    name: str
    price: int
    description: str
    main_image: str
    images: str
    active: bool
    stock: int
    category: str

class CartItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(default=None, foreign_key="product.id")
    user_id: int = Field(default=None, foreign_key="user.id")

    quantity:int

class _ReqProductSnapshot(BaseModel):
    product_id: str
    quantity: int

class _TransactionProductSnapshot(BaseModel):
    product: Product
    quantity: int

class TransactionProductsSnapshot(BaseModel):
    snapshots: List[_TransactionProductSnapshot]

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: int = Field(default=None, foreign_key="user.id") # id of the user who initiated the transaction
    product_snapshots: str # the products snapshots are going to be JSON serialized
    date: float # utc timestamp
    payment_method: str # fallback to -> Union["momo", "credit-card"]
    amount_total: int
    status: str  # fallback to -> Union["Pending","Processing", "Complete", "Cancelled"]
