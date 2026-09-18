from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    status_id = Column(Integer, ForeignKey('status.id'))
    created_at = Column(DateTime(timezone=True),
                        default=datetime.now(timezone.utc))

    user = relationship("Users", back_populates="orders")
    status = relationship("Status", back_populates="orders")
    order_items = relationship("OrderItems", back_populates="order")

    def __str__(self):
        return f"Order {self.id} - {self.status_id}"