

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from coverletter.main import SessionLocal
from coverletter.services.users import get_users
from coverletter.shemas.users import UserSchema

router = APIRouter(
    prefix="/users",
)


def get_db():
    yield SessionLocal()


@router.get("/")
def get_all_users(session: Session = Depends(get_db)) -> list[UserSchema]:
    users: list[UserSchema] = []
    for user in get_users(session):
        users.append(UserSchema(id=user.id, name=user.name, email=user.email, credits=user.credits))
    return users

