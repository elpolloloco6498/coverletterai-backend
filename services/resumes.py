from typing import List

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from models.resumes import Resume
from models.users import User
from services.parsing import extract_text_from_pdf
from services.users import get_user
from shemas.resumes import ResumeSchema, CreateResumeSchema


def get_resume(session: Session, id: int) -> Resume:
    stmt = select(Resume).filter_by(id=id)
    try:
        return session.scalars(stmt).one()
    except NoResultFound:
        return False


def add_resume(session: Session, user_id: str, resume_schema: CreateResumeSchema) -> Resume:
    user: User = get_user(session, user_id)
    resume = Resume(
        name=resume_schema.name,
        text=resume_schema.text,
    )
    user.resumes.append(resume)
    return resume


def add_resume_from_file(session: Session, file: UploadFile, user_id: str) -> Resume:
    resume_text = extract_text_from_pdf(file.file)
    filename = file.filename
    resume = add_resume(session, user_id, CreateResumeSchema(
        name=filename,
        text=resume_text,
    ))
    return resume


def delete_resume(session: Session, id: int):
    resume = get_resume(session, id)
    session.delete(resume)
    return resume

