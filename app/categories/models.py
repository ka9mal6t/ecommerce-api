from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description  = Column(String, unique=False, nullable=True)

    products = relationship("Products", back_populates="category")

    def __str__(self):
        return f"Category {self.id} - {self.name}"