
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class User(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    full_name: str
    email: str
    password: str
    email_verified: Optional[bool] = False
    profile: Optional["Profile"] = Relationship(back_populates="user")
    orders: List["Order"] = Relationship(back_populates="user")
