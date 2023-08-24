from sqlmodel import select, Session
from database import create_db_and_tables, engine
from models import User, Shop, Product
from typing import Annotated
import secrets
from fastapi import FastAPI, File, UploadFile, Form, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import StreamingResponse

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.on_event("startup")
async def on_startup():
    create_db_and_tables()
    
@app.get("/")
def _index():
    return { "msg": "Shopping should be a piece of kek" }

@app.post("/Users/")
async def create_user(user: User, token: Annotated[str, Depends(oauth2_scheme)]):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    
@app.get("/users/")
async def read_users(token: Annotated[str, Depends(oauth2_scheme)]):
    with Session(engine) as session: 
        Users = session.exec(select(User)).all()
        return Users
    
@app.post("/shops/")
async def create_shop(shop:Shop, token: Annotated[str, Depends(oauth2_scheme)]):
    with Session(engine) as session:
        session.add(shop)
        session.commit()
        session.refresh(shop)
        return shop
    
@app.get("/Shops/")
async def read_shops(token: Annotated[str, Depends(oauth2_scheme)]):
    with Session(engine) as session:
        Shops = session.exec(select(Shop)).all()
        return Shops
    
@app.post("/products/")
async def  create_product(product:Product, token: Annotated[str, Depends(oauth2_scheme)]):
    with Session(engine) as session:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product
    
@app.get("/Products/")
async def read_products(token: Annotated[str, Depends(oauth2_scheme)]):
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
        return products

@app.post("/upload")
async def upload_file(
    file: Annotated[UploadFile, File()],
    token: Annotated[str, Depends(oauth2_scheme)]
):
    try:
        if file.content_type:
            extension = file.content_type.split("/")
            content = await file.read()
            disk_filename = f"{secrets.token_urlsafe(10)}.{extension[-1]}"

            # write the file to disk
            with open(disk_filename, "wb") as image_file:
                image_file.write(content)
            return { "msg": f"wrote file to {disk_filename}" }
    except:
        return { "msg": "Failed" }

