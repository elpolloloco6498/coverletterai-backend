from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from models.users import User
from shemas.users import CreateUserSchema


class UserAlreadyExists(Exception):
    pass


def get_all_users(session: Session) -> Sequence[User]:
    stmt = session.scalars(select(User)).all()
    return stmt


def get_user(session: Session, id: str | None = None, name: str | None = None, email: str | None = None) -> User | bool:
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


def upsert_user(session: Session, user_schema: CreateUserSchema) -> User | None:
    if not get_user(session, user_schema.id):
        user = User(**user_schema.dict())
        session.add(user)
        return user


def remove_user(session: Session, id: str) -> None:
    if get_user(session, id):
        stmt = delete(User).where(User.id == id)
        session.execute(stmt)


def update_user_credit(session: Session, user_id, amount) -> None:
    session.query(User).filter(User.id == user_id).update({"credits": amount})


def add_user_credit(session: Session, user_id, amount) -> None:
    user_credits = get_user(session, user_id).credits
    update_user_credit(session, user_id, user_credits + amount)


def supply_credits(session: Session, user_id, product_id) -> None:
    product_credits = {
        "product1": 5,
        "product2": 10,
        "product3": 20,
    }
    add_user_credit(session, user_id, product_credits[product_id])


