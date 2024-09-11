from enum import Enum as PythonEnum

from database import Base
from sqlalchemy import (
    TIMESTAMP,
    Column,
    Date,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    text,
)
from sqlalchemy.orm import relationship


class UserRole(PythonEnum):
    User = "User"
    Admin = "Admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(LargeBinary, nullable=False)
    role = Column(String, nullable=False, default=UserRole.User.value)
    created_at = Column(
        TIMESTAMP(timezone=False), nullable=False, server_default=text("now()")
    )
    standups = relationship("Standup", back_populates="user")


class Standup(Base):
    __tablename__ = "standups"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(String, nullable=False)
    date = Column(Date, nullable=False)

    user = relationship("User", back_populates="standups")
