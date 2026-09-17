from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description  = Column(String, nullable=True)

    orders = relationship("Orders", back_populates="status")

    def __str__(self):
        return f"Status {self.id} - {self.name}"