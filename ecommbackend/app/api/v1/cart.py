from fastapi import ApiRouter, Depends, HttpExceution, Query
from app.core.database import SessionLocal
from sqlalchemy.orm import Session
from app.schemas.user import AddToCart
from app.services.auth_service import add_cart_item


router = ApiRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/addToCart")
def add_to_cart(payload: AddToCart, db: Session = Depends(get_db)):
    user_id = 1
    return add_cart_item(db, user_id, payload.product_id, payload.quantity)


@router.post("/cart/items")
def get_queried_items(
    product_id: int = Query(...),
    quantity: int = Query(default=1),
    db: Session = Depends(get_db),
):
    return {product_id}
