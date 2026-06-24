import os
from sqlmodel import SQLModel, create_engine, Session


# database_url = os.getenv("DATABASE_URL")
database_url = "postgresql+psycopg2://server:courage@localhost:5432/crud_db"

engine = create_engine(database_url, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine) 

def get_session():
    with Session(engine) as session:
        yield session
