from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    contact_phone: Optional[int] = None
    momo: Optional[int] = None
    profile_image: str
    location: str
    date_of_birth: str
    active: bool

class Shop(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    contact_phone: Optional[int] = None
    momo: Optional[int] = None
    profile_image: str
    location: str
    date_of_birth: str
    active: bool

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    contact_phone: Optional[int] = None
    momo: Optional[int] = None
    profile_image: str
    location: str
    date_of_birth: str
    active: bool



# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)


# def create_users():
#     user_1 = User(name="Deadpond", email="Dive Wilson")
#     user_2 = User(name="Spider-Boy", email="Pedro Parqueador")
#     user_3 = User(name="Rusty-Man", email="Tommy Sharp", momo=000000000 )
#     user_4 = User(name="Tarantula", email="Natalia Roman-on", momo=000000000)
#     user_5 = User(name="Black Lion", email="Trevor Challa", momo=000000000)
#     user_6 = User(name="Dr. Weird", email="Steve Weird", momo=000000000)
#     user_7 = User(name="Captain North America", email="Esteban Rogelios", momo=000000000)

#     with Session(engine) as session:
#         session.add(user_1)
#         session.add(user_2)
#         session.add(user_3)
#         session.add(user_4)
#         session.add(user_5)
#         session.add(user_6)
#         session.add(user_7)

#         session.commit()
        
# def update_users():
#     with Session(engine) as session:
#         statement = select(User).where(User.name == "Spider-Boy")  # 
#         results = session.exec(statement)  # 
#         user = results.one()  # 
#         print("User:", user)  # 

#         user.age = 16  # 
#         session.add(user)  # 
#         session.commit()  # 
#         session.refresh(user)  # 
#         print("Updated user:", user)  # 


# def main():
#     create_db_and_tables()
#     create_users()
#     update_users()


if __name__ == "__main__":
    main()
    