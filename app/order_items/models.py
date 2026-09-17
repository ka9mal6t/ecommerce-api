from sqlalchemy import Column, Integer, Numeric, ForeignKey, Computed
from sqlalchemy.orm import relationship

from app.database import Base


class OrderItems(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, default=1)

    product = relationship("Products")
    order = relationship("Orders", back_populates="order_items")

    def __str__(self):
        return f"Order {self.order_id} ItemsId {self.product_id}"