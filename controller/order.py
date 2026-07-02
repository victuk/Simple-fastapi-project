from fastapi import APIRouter, Depends
from model.users import User
from authorization.get_current_user import CheckRole


order_route = APIRouter(
    prefix="/orders",
    tags=["orders"]
)


@order_route.get("/")
def get_order_list(current_user: User = Depends(CheckRole(["admin", "user"]))):
    print("current_user", current_user)
    return [
        {
            "id": 1,
            "product_name": "Power bank"
        }
    ]

