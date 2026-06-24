from fastapi import APIRouter


order_route = APIRouter(
    prefix="/orders",
    tags=["orders"]
)


@order_route.get("/")
def get_order_list():
    return [
        {
            "id": 1,
            "product_name": "Power bank"
        }
    ]

