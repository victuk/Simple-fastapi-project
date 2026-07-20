
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from model.users import User
from model.order_category import OrderCategory

class Category(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    name: str
    slug: str

    orders: List["Order"] = Relationship(back_populates="categories", link_model=OrderCategory)
