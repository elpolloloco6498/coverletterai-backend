

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from services.letters import delete_letter, get_letter
from shemas.letters import LetterSchema

router = APIRouter(
    prefix="/letters",
)


def get_db():
    yield SessionLocal()


@router.get("/remove/{letter_id}")
def remove(letter_id: int, session: Session = Depends(get_db)):
    letter = delete_letter(session, letter_id)
    session.commit()


@router.get("/{id}")
def get(id: str, session: Session = Depends(get_db)) -> LetterSchema | None:
    letter = get_letter(session, id)
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

