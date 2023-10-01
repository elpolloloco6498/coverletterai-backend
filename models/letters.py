import datetime

from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Letter(Base):
    __tablename__ = "letter"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_name: Mapped[str] = mapped_column(String(255))
    job_title: Mapped[str] = mapped_column(String(255))
    language: Mapped[str] = mapped_column(String(255))
    writing_style: Mapped[str] = mapped_column(String(255))
    generation_date: Mapped[datetime.date] = mapped_column(Date)
    text: Mapped[str] = mapped_column(String(10000))
    user_id = mapped_column(ForeignKey("user.id"))

    def __repr__(self):
        return f"id: {self.id}, company_name: {self.company_name}, job_title: {self.job_title}"
