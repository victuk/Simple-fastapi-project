from fastapi import APIRouter, Depends
from model.users import User
from authorization.get_current_user import CheckRole
from pydantic import BaseModel
from service.order import (
    create_order,
    get_order_list,
    create_category,
    get_category_list,
    get_order_category
    )
from database import get_session
from sqlmodel import Session
from typing import List

order_route = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

class CreateOrder(BaseModel):
    address: str
    weight: str
    category_ids: List[str]


@order_route.post("/")
def create_order_function(create_order_details: CreateOrder, current_user: User = Depends(CheckRole(["user"])), session: Session = Depends(get_session)):
    return create_order(create_order_details, session, current_user)
    
    

@order_route.get("/")
def get_orders(session: Session = Depends(get_session)):
    return get_order_list(session)


class CategoryClass(BaseModel):
    name: str

@order_route.post("/categories")
def create_category_controller(category: CategoryClass, session: Session = Depends(get_session)):
    return create_category(category.name, session)

@order_route.get("/categories")
def get_categories_controller(session: Session = Depends(get_session)):
    return get_category_list(session)

@order_route.get("/order-categories")
def order_categories_controller(session: Session = Depends(get_session)):
    return get_order_category(session)
