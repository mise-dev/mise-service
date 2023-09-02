from sqlmodel import select, Session
from database import create_db_and_tables, engine
from models import User, Shop, Product
from typing import Annotated, Optional, List
import secrets
from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import StreamingResponse
from auth import decode_token, hash_password, create_token, verify_password
from search import search_product
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: Annotated[dict, Depends(oauth2_scheme)]):
    token_data = decode_token(token)

    with Session(engine) as session:
        user = session.exec(select(User).where(User.name == token_data.get("name"))).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

@app.on_event("startup")
async def on_startup():
    create_db_and_tables()
    
@app.post("/search")
async def search_products( query: str) -> List[Product]:
    
    with Session(engine) as session:
        products = session.exec(select(Product).where((Product.name.ilike("%{}%".format(query))) | (Product.description.ilike("%{}%".format(query)))))

        return list(products)

@app.post("/token")
async def _auth(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.name == form_data.username)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password",
        )
    if not verify_password(user.password, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong password or username",
        )
    token = create_token({ "name": user.name, "uuid": user.id })
    return { "access_token": token, "token_type": "bearer" }


@app.get("/")
def _index():
    return { "msg": "Shopping should be a piece of kek" }

@app.post("/users/")
async def create_user(user: User):
    user.password = hash_password(user.password)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    
@app.get("/users/")
async def read_users():
    with Session(engine) as session: 
        Users = session.exec(select(User)).all()
        return Users
    
@app.post("/shops/")
async def create_shop(shop:Shop, user: Annotated[dict, Depends(get_current_user)]):
    with Session(engine) as session:
        session.add(shop)
        session.commit()
        session.refresh(shop)
        return shop
    
@app.get("/Shops/")
async def read_shops(user: Annotated[dict, Depends(get_current_user)]):
    with Session(engine) as session:
        Shops = session.exec(select(Shop)).all()
        return Shops
    
@app.post("/products/")
async def create_product(product:Product, user: Annotated[dict, Depends(get_current_user)]):
    with Session(engine) as session:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product
    
@app.get("/Products/")
async def read_products(user: Annotated[dict, Depends(get_current_user)]):
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
        return products

@app.post("/upload")
async def upload_file(
    file: Annotated[UploadFile, File()],
    user: Annotated[dict, Depends(get_current_user)]
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

