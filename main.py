from sqlmodel import select, Session, or_, and_, update
from database import create_db_and_tables, engine
from models import (
    CartItem,
    User,
    Shop,
    Product,
    Transaction,
    _TransactionProductSnapshot,
    TransactionProductsSnapshot,
    _ReqProductSnapshot,
)
from typing import Annotated, Tuple, List
import secrets
from fastapi import (
    FastAPI,
    File,
    UploadFile,
    Form,
    Depends,
    HTTPException,
    status,
    Query,
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from auth import decode_token, hash_password, create_token, verify_password
import os
from datetime import datetime, timezone

app = FastAPI()
# add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Annotated[dict, Depends(oauth2_scheme)]):
    token_data = decode_token(token)

    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.name == token_data.get("name"))
        ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    with Session(engine) as session:
        user_shop = session.exec(select(Shop).where(Shop.user_id == user.id)).first()
        if not user_shop:
            user_shop = {}
    # convert the user shop to dict if not dict
    user_shop = user_shop.dict() if isinstance(user_shop, Shop) else user_shop
    _user_shop = {}
    # prepend all shop property keys with shop_ to distinguish from user info
    for key in user_shop.keys():
        _user_shop[f"shop_{key}"] = user_shop[key]

    # merge the two results
    return user.dict() | _user_shop


@app.on_event("startup")
async def on_startup():
    if not os.path.isdir("images"):
        os.mkdir("images")
    create_db_and_tables()


@app.post("/search")
async def search_products(query: str) -> List[Product]:
    with Session(engine) as session:
        products = session.exec(
            select(Product).where(
                or_(Product.name.ilike("%{}%".format(query))),
                (Product.description.ilike("%{}%".format(query))),
            )
        )

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
    token = create_token({"name": user.name, "uuid": user.id})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/auth")
async def _authenticate(user: Annotated[dict, Depends(get_current_user)]):
    return user

@app.get("/")
def _index():
    return {"msg": "Shopping should be a piece of kek"}


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
async def create_shop(shop: Shop, user: Annotated[dict, Depends(get_current_user)]):
    with Session(engine) as session:
        session.add(shop)
        session.commit()
        session.refresh(shop)
        return shop


@app.get("/shops/")
async def read_shops(user: Annotated[dict, Depends(get_current_user)]):
    with Session(engine) as session:
        Shops = session.exec(select(Shop)).all()
        return Shops


@app.get("/shops/products")
async def read_shop_products(shop_id: int, user: Annotated[dict, Depends(get_current_user)]):
    with Session(engine) as session:
        query = select(Product).where(Product.shop_id == shop_id)
        products = session.exec(query).all()
        return products

@app.post("/products/")
async def create_product(
    product: Product, user: Annotated[dict, Depends(get_current_user)]
):
    print(product)
    with Session(engine) as session:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product


@app.get("/products/")
async def read_products(user: Annotated[dict, Depends(get_current_user)]):
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
        return products

@app.get("/products/{product_id}")
async def read_product(
    product_id: int,
    user: Annotated[dict, Depends(get_current_user)]
):
    with Session(engine) as session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product


@app.put("/products/{product_id}")
async def update_product(
    product_id: int,
    product: Product,
    user: dict = Depends(get_current_user)
):
    with Session(engine) as session:
        db_product = session.get(Product, product_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")

         # Create a new product instance with updated values
        updated_product_data = product.dict(exclude_unset=True)
        updated_product = Product(**updated_product_data)

        # Update the database with the new product
        session.merge(updated_product)
        session.commit()

        return updated_product

@app.delete("/products/{product_id}")
async def delete_product(
    product_id: int,
    user: Annotated[dict, Depends(get_current_user)]
):
    with Session(engine) as session:
        db_product = session.get(Product, product_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        session.delete(db_product)
        session.commit()
        return {"message": "Product deleted"}


@app.post("/upload")
async def upload_file(
    file: Annotated[UploadFile, File()],
    user: Annotated[dict, Depends(get_current_user)],
):
    try:
        if file.content_type:
            extension = file.content_type.split("/")
            content = await file.read()
            disk_filename = f"{secrets.token_urlsafe(10)}.{extension[-1]}"

            # write the file to disk
            with open(f"images/{disk_filename}", "wb") as image_file:
                image_file.write(content)
            return {"image_uri": f"/images/{disk_filename}", "msg": "Success"}
    except:
        return {"msg": "Failed"}

@app.get("/images/{image_uri}")
async def _load_image(image_uri):
    def read_image_file():
        with open(f"images/{image_uri}", "rb") as image_file:
            yield from image_file
    return StreamingResponse(read_image_file())

# returns all transactions carried out by the user
@app.get("/transaction")
async def list_transactions(user: Annotated[dict, Depends(get_current_user)]):
    with Session(engine) as session:
        return session.exec(select(Transaction).where(Transaction.uid == user.id)).all()


# try to enforce payment method to Union["momo", "credit-card"]
@app.post("/transaction")
async def create_transaction(
    products: List[_ReqProductSnapshot],
    payment_method: str,
    user: Annotated[dict, Depends(get_current_user)],
):
    with Session(engine) as session:
        # get the products
        _products = []
        for psnap in products:
            _product = session.exec(
                select(Product).where(Product.id == psnap.product_id)
            ).one()
            _products.append(
                _TransactionProductSnapshot(product=_product, quantity=psnap.quantity)
            )

        amount_total = sum(list(map(lambda x: x.product.price * x.quantity, _products)))

        # create the products snapshot
        tp_snapshots = TransactionProductsSnapshot(snapshots=_products)

        # save the transaction to db
        transaction = Transaction(
            uid=user.id,
            date=datetime.now(timezone.utc).timestamp(),
            payment_method=payment_method,
            status="Processing",
            product_snapshots=tp_snapshots.json(),  # the snapshots are stored as json-serializable
            amount_total=amount_total,
        )

        session.add(transaction)
        session.commit()
        session.refresh(transaction)

        return {"success": True, "data": transaction}


@app.post("/transaction/cancel")
async def cancel_transaction(transaction_id: int, user: Annotated[dict, Depends(get_current_user)]):
    with Session(engine) as session:
        transaction = session.exec(
            select(Transaction).where(and_(Transaction.id == transaction_id, Transaction.uid == user.id))
        ).one()
        transaction.status = "Cancelled"

        session.add(transaction)
        session.commit()
        session.refresh(transaction)

    return {"success": True}


@app.get("/cart")
async def get_cart(user: Annotated[dict, Depends(get_current_user)]):
    
    # return {"data": CartItem}
    with Session(engine) as session:
        cart = session.exec(select(CartItem)).all()
        return cart



@app.post("/cart")
async def create_cart(
    cart: CartItem, user: Annotated[dict, Depends(get_current_user)]
):
    with Session(engine) as session:
        session.add(cart)
        session.commit()
        session.refresh(cart)
        return cart

@app.put("/cart/{id}")
async def update_cart(
    id: int,
    cart: CartItem,
    user: dict = Depends(get_current_user)  
):
 with Session(engine) as session:
        db_product = session.get(CartItem, id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")

         # Create a new product instance with updated values
        updated_product_data = cart.dict(exclude_unset=True)
        updated_product = CartItem(**updated_product_data)

        # Update the database with the new product
        session.merge(updated_product)
        session.commit()

        return updated_product

