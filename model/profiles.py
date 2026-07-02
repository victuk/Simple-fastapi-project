
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from model.users import User

class Profile(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    
    username: str
    address: str
    
    user_id: int = Field(foreign_key="user.id", unique=True)
    user: Optional[User] = Relationship(back_populates="profile")