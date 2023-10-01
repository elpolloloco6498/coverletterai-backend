from typing import List

from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    credits: Mapped[int] = mapped_column(Integer)
    letters: Mapped[list["Letter"]] = relationship("Letter", cascade="all, delete-orphan", backref="user")

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"
