from sqlalchemy import select
from sqlalchemy.orm import Session

from coverletter.models.users import User


def get_users(session: Session) -> list[User]:
    stmt = session.scalars(select(User)).all()
    return stmt


def get_user(session: Session, id: int | None=None, name: str | None=None, email: str | None=None, credits: int | None=None):
    pass


def upsert_user(session: Session):
    pass


def remove_user(session: Session):
    pass
