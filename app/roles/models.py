from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description  = Column(String, nullable=True)

    users = relationship("Users", back_populates="role")

    def __str__(self):
        return f"Role {self.id} - {self.name}"