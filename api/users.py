from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from services.users import upsert_user, get_all_users, remove_user, get_user
from shemas.letters import LetterSchema
from shemas.resumes import ResumeSchema
from shemas.users import UserSchema

router = APIRouter(
    prefix="/users",
)


def get_db():
    yield SessionLocal()


@router.get("/")
def get_all(session: Session = Depends(get_db)) -> list[UserSchema]:
    all_users: List[UserSchema] = []
    for user in get_all_users(session):
        letters = [
            LetterSchema(
                id=letter.id,
                user_id=letter.user_id,
                company_name=letter.company_name,
                job_title=letter.job_title,
                language=letter.language,
                writing_style=letter.writing_style,
                generation_date=letter.generation_date,
                text=letter.text,
            )
            for letter in user.letters
        ]

        resumes = [
            ResumeSchema(
                id=resume.id,
                name=resume.name,
                text=resume.text,
            )
            for resume in user.resumes
        ]

        all_users.append(UserSchema(id=user.id, name=user.name, email=user.email, credits=user.credits, letters=letters, resumes=resumes))
    return all_users


@router.get("/user/{user_id}")
def get(user_id: str, session: Session = Depends(get_db)):
    user = get_user(session, id=user_id)
    letters = [
        LetterSchema(
            id=letter.id,
            user_id=letter.user_id,
            company_name=letter.company_name,
            job_title=letter.job_title,
            language=letter.language,
            writing_style=letter.writing_style,
            generation_date=letter.generation_date,
            text=letter.text,
        )
        for letter in user.letters
    ]
    resumes = [
        ResumeSchema(
            id=resume.id,
            name=resume.name,
            text=resume.text,
        )
        for resume in user.resumes
    ]
    if user:
        return UserSchema(id=user.id, name=user.name, email=user.email, credits=user.credits, letters=letters, resumes=resumes)


@router.post("/upsert")
def upsert(upsert_user_schema: UserSchema, session: Session = Depends(get_db)):
    user = upsert_user(session, upsert_user_schema)
    if user:
        session.commit()
        return UserSchema(id=user.id, name=user.name, email=user.email, credits=user.credits, letters=user.letters, resumes=user.resumes)


@router.get("/remove/{user_id}")
def remove(user_id: str, session: Session = Depends(get_db)):
    user = get_user(session, id=user_id)
    remove_user(session, user_id)
    session.commit()
    return UserSchema(id=user.id, name=user.name, email=user.email, credits=user.credits, letters=user.letters)
