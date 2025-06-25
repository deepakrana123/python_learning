from app.models.user import Cart
from sqlalchemy.orm import Session


def add_cart_item(db: Session, product_id: str, quantity: int):
    cart = Cart(product_id, quantity)
    db.add(cart)
    db.commit()
    # db.refresh(cart)
    return cart


def get_cart_item(db: Session, user_id):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if cart:
        return cart
    return None


def delete_cart_item(db: Session, cart_id):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if cart:
        raise Exception(status_code=404, detail="Cart item not found")
    db.delete(cart)
    db.commit()
    return {"detail": "Cart item deleted"}
