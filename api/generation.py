from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.users import get_db
from services.generation import generate_cover_letter, generate_dummy_cover_letter
from shemas.coverletter import CreateCoverLetterSchema

router = APIRouter(
    prefix="/generation",
)


@router.get("/")
def version():
    return {"version": "1.0"}


@router.post("/generation")
def create_cover_letter(coverletter_schema: CreateCoverLetterSchema, session: Session = Depends(get_db)):
    cover_letter = generate_cover_letter(session, coverletter_schema)
    return cover_letter
