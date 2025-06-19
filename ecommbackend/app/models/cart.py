from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base


class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer)
    quantity = Column(Integer)
``