from model.order import Order
from model.users import User
from model.category import Category
from model.order_category import OrderCategory
from sqlmodel import select
from sqlalchemy.orm import selectinload, joinedload

def create_order(create_order_details, session, user):

    o = create_order_details.model_dump()
    order = Order()
    order.address = o["address"]
    order.weight = o["weight"]    
    order.user = session.get(User, user["sub"])

    if len(o["category_ids"]) > 0:
        order.categories = session.exec(select(Category).where(Category.id.in_(o["category_ids"]))).all()
    
    session.add(order)
    session.commit()
    session.refresh(order)
    
    return order


def get_order_list(session):
    order = select(Order)
    result = session.exec(order).all()
    return result


def create_category(category: str, session):
    cat = Category()
    cat.name = category
    cat.slug = category.lower().replace(" ", "-", count=-1)
    
    session.add(cat)
    session.commit()
    session.refresh(cat)
    
    return cat
    
    
def get_category_list(session):
    category = select(Category) 
    result = session.exec(category).all()
    return result


def get_order_category(session):
    res = select(OrderCategory).options(
        joinedload(OrderCategory.category_id),
        joinedload(OrderCategory.order_id)
    )
    
    value = session.exec(res).all()
    return value
