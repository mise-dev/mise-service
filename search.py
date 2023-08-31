from sqlmodel import select, Session
from models import Product

def search_product(query: str, db:Session):
    product= db.query(Product).filter(Product.title.contains(query))
    return product