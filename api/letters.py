import tempfile

from fastapi import APIRouter, Depends
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from database import SessionLocal
from models.letters import Letter
from services.letters import delete_letter, get_letter, modify_letter
from services.utils import text_to_pdf
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


@router.get("/download/{letter_id}")
def download(letter_id: int, session: Session = Depends(get_db)):
    letter: Letter = get_letter(session, letter_id)
    pdf_buffer = text_to_pdf(letter.text)
    filename = f"{letter.company_name}_{letter.job_title}_{letter.generation_date}.pdf"
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(pdf_buffer)
        temp_file.seek(0)
        # Serve the temporary file
        return FileResponse(
            temp_file.name,
            media_type="application/pdf",
            headers={"filename": filename}
        )
