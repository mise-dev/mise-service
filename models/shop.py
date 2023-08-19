from typing import Optional
from sqlmodel import Field, SQLModel

class Shop(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user: int = Field(foreign_key=True)
    name: str
    description: str
    shop_image: str # uri to cloudflare image
    momo_number: str # should ref the momo number of the user owning the shop
