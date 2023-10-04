from datetime import datetime

from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Resume(Base):
    __tablename__ = "resume"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    text: Mapped[str] = mapped_column(String(10000))
    user_id = mapped_column(ForeignKey("user.id"))

    def __repr__(self):
        return f"id: {self.id}, company_name: {self.name}"
