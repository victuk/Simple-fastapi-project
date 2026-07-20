
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from model.users import User
from model.order_category import OrderCategory
from model.category import Category

class Order(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    address: str
    weight: str

    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="orders")
    
    categories: List[Category] = Relationship(back_populates="orders", link_model=OrderCategory)
    
    # orders: User = Relationship(back_populates="order")
