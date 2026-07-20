
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from model.users import User
from model.order_category import OrderCategory
from model.category import Category

class UserSession(SQLModel, table=True):
    
    id: int = Field(default=None, primary_key=True)
    
    user_id: int
    refresh_token: str
