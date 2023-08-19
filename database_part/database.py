from sqlmodel import Field, Session, SQLModel, create_engine, select
from models import User
DATABASE_URL = "sqlite:///./mise_app.db"

connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

def create_users():
    user_1 = User(name="Deadpond", email="Dive Wilson", momo=000000000, contact_phone=000000000, profile_image="hello", location="hello", date_of_birth="hello", active=0 )
    user_2 = User(name="Spider-Boy", email="Pedro Parqueador", momo=000000000, contact_phone=000000000, profile_image="hello", location="hello", date_of_birth="hello", active=0)
    user_3 = User(name="Rusty-Man", email="Tommy Sharp", momo=000000000, contact_phone=000000000, profile_image="hello", location="hello", date_of_birth="hello", active=0 )
    user_4 = User(name="Tarantula", email="Natalia Roman-on", momo=000000000, contact_phone=000000000, profile_image="hello", location="hello", date_of_birth="hello", active=0)
    user_5 = User(name="Black Lion", email="Trevor Challa", momo=000000000, contact_phone=000000000, profile_image="hello", location="hello", date_of_birth="hello", active=0)
    user_6 = User(name="Dr. Weird", email="Steve Weird", momo=000000000, contact_phone=000000000, profile_image="hello", location="hello", date_of_birth="hello", active=0)
    user_7 = User(name="Captain North America", email="Esteban Rogelios", momo=000000000, contact_phone=000000000, profile_image="hello", location="hello", date_of_birth="hello", active=0)

    with Session(engine) as session:
        session.add(user_1)
        session.add(user_2)
        session.add(user_3)
        session.add(user_4)
        session.add(user_5)
        session.add(user_6)
        session.add(user_7)

        session.commit()
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

