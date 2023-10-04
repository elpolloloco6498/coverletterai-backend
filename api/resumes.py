from typing import List, Annotated

from fastapi import APIRouter, UploadFile, Depends, Form
from sqlalchemy.orm import Session

from database import SessionLocal
from models.resumes import Resume
from services.resumes import add_resume_from_file, delete_resume
from shemas.resumes import ResumeSchema

router = APIRouter(
    prefix="/resumes",
)


def get_db():
    yield SessionLocal()


@router.post("/add-resume")
async def add_resume(file: UploadFile, user_id: Annotated[str, Form()], session: Session = Depends(get_db)) -> ResumeSchema:
    resume: Resume = add_resume_from_file(session, file, user_id)
    session.commit()
    return ResumeSchema(
        id=resume.id,
        name=resume.name,
        text=resume.text,
    )


@router.get("/remove/{resume_id}")
async def remove_resume(resume_id: int, session: Session = Depends(get_db)) -> ResumeSchema:
    resume = delete_resume(session, resume_id)
    session.commit()
    return ResumeSchema(
        id=resume.id,
        name=resume.name,
        text=resume.text,
    )

