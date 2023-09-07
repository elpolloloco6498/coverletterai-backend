
from fastapi import APIRouter, UploadFile

from services.parsing import extract_text_from_pdf

router = APIRouter(
    prefix="/parsing",
)


@router.get("/")
def version():
    return {"version": "1.0"}


@router.post("/extract-text-pdf")
async def extract_text_pdf(file: UploadFile):
    text = extract_text_from_pdf(file.file)
    return text
