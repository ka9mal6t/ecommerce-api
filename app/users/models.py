from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hash_password = Column(String, nullable=False)

    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship("Roles", back_populates="users")
    orders = relationship("Orders", back_populates="user")

    def __str__(self):
        return f"User {self.id} - {self.username}"