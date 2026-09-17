from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from app.database import Base


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    name = Column(String, unique=True, nullable=False)
    description = Column(String, unique=False, nullable=True)
    price = Column(Numeric(10, 2), unique=False, nullable=True)
    image_url = Column(String, unique=False, nullable=True)

    category = relationship("Categories", back_populates="products")

    def __str__(self):
        return f"Product {self.id} - {self.name}"