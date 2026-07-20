
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from model.users import User

class OrderCategory(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    order_id: int = Field(foreign_key="order.id", primary_key=True)
    category_id: int = Field(foreign_key="category.id", primary_key=True)
