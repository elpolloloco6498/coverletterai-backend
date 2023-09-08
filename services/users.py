from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from models.users import User
from shemas.users import UserSchema


class UserAlreadyExists(Exception):
    pass


def get_all_users(session: Session) -> Sequence[User]:
    stmt = session.scalars(select(User)).all()
    return stmt


def get_user(session: Session, id: str | None = None, name: str | None = None, email: str | None = None):
    stmt = select(User)
    if id is not None:
        stmt = stmt.filter_by(id=id)
    if name is not None:
        stmt = stmt.filter_by(name=name)
    if email is not None:
        stmt = stmt.filter_by(email=email)
    try:
        return session.scalars(stmt).one()
    except NoResultFound:
        return False


def upsert_user(session: Session, user_schema: UserSchema):
    if not get_user(session, user_schema.id):
        user = User(**user_schema.dict())
        session.add(user)
        return user


def remove_user(session: Session, id: str) -> None:
    if get_user(session, id):
        stmt = delete(User).where(User.id == id)
        session.execute(stmt)
