from sqlmodel import select, Session
from database import create_db_and_tables, engine
from models import User, Shop, Product

from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
@app.post("/Users/")
def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    
@app.get("/users/")
def read_users():
    with Session(engine) as session: 
        Users = session.exec(select(User)).all()
        return Users
    
@app.post("/shops/")
def  create_shop(shop:Shop):
    with Session(engine) as session:
        session.add(shop)
        session.commit()
        session.refresh(shop)
        return shop
    
@app.get("/Shops/")
def read_shops():
    with Session(engine) as session:
        Shops = session.exec(select(Shop)).all()
        return Shops
    
@app.post("/products/")
def  create_shop(product:Product):
    with Session(engine) as session:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product
    
@app.get("/Products/")
def read_shops():
    with Session(engine) as session:
        Products = session.exec(select(Product)).all()
        return Products