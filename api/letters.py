

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from services.letters import delete_letter, get_letter, modify_letter
from shemas.letters import LetterSchema, UpdateLetterSchema

router = APIRouter(
    prefix="/letters",
)


def get_db():
    yield SessionLocal()


@router.get("/remove/{letter_id}")
def remove(letter_id: int, session: Session = Depends(get_db)) -> LetterSchema | None:
    letter = delete_letter(session, letter_id)
    session.commit()
    if letter:
        return LetterSchema(
            id=letter.id,
            user_id=letter.user_id,
            company_name=letter.company_name,
            job_title=letter.job_title,
            language=letter.language,
            writing_style=letter.writing_style,
            generation_date=letter.generation_date,
            text=letter.text,
        )


@router.get("/{letter_id}")
def get(letter_id: int, session: Session = Depends(get_db)) -> LetterSchema | None:
    letter = get_letter(session, letter_id)
    if letter:
        return LetterSchema(
            id=letter.id,
            user_id=letter.user_id,
            company_name=letter.company_name,
            job_title=letter.job_title,
            language=letter.language,
            writing_style=letter.writing_style,
            generation_date=letter.generation_date,
            text=letter.text,
        )


@router.post("/modify/{letter_id}")
def modify(letter_id: int, letter_schema: UpdateLetterSchema, session: Session = Depends(get_db)) -> LetterSchema | None:
    letter = modify_letter(session, letter_id, letter_schema)
    session.commit()
    if letter:
        return LetterSchema(
            id=letter.id,
            user_id=letter.user_id,
            company_name=letter.company_name,
            job_title=letter.job_title,
            language=letter.language,
            writing_style=letter.writing_style,
            generation_date=letter.generation_date,
            text=letter.text,
        )

