
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class User(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    full_name: str
    email: str
    password: str
    profile: Optional["Profile"] = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})
