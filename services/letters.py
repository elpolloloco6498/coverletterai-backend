from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from models.letters import Letter
from models.users import User
from services.users import get_user
from shemas.letters import CreateLetterSchema


def get_letter(session: Session, id: int):
    stmt = select(Letter).filter_by(id=id)
    try:
        return session.scalars(stmt).one()
    except NoResultFound:
        return False


def add_letter(session: Session, user_id: int, letter_schema: CreateLetterSchema) -> User:
    user: User = get_user(session, user_id)
    letter = Letter(**letter_schema.dict())
    user.letters.append(letter)
    return user


def modify_letter(session: Session, id: int, letter_schema: CreateLetterSchema) -> Letter:
    letter: Letter = get_letter(session, id)
    letter.company_name = letter_schema.company_name
    letter.job_title = letter_schema.job_title
    letter.language = letter_schema.language
    letter.writing_style = letter_schema.writing_style
    letter.generation_date = letter_schema.generation_date
    letter.text = letter_schema.text
    return letter


def delete_letter(session: Session, id: int) -> Letter:
    letter = get_letter(session, id)
    saved_letter = letter
    session.delete(letter)
    return saved_letter
