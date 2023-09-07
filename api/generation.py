from fastapi import APIRouter

from services.generation import generate_cover_letter, generate_dummy_cover_letter
from shemas.coverletter import CreateCoverLetterSchema

router = APIRouter(
    prefix="/generation",
)


@router.get("/")
def version():
    return {"version": "1.0"}


@router.post("/generation")
def create_cover_letter(coverletter_schema: CreateCoverLetterSchema):
    cover_letter = generate_cover_letter(coverletter_schema)
    # cover_letter = generate_dummy_cover_letter()
    return cover_letter
