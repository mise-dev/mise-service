from sqlmodel import SQLModel, create_engine
from decouple import config

DATABASE_URL=config("DATABASE_URL")

connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
