
from enum import Enum

from pydantic import BaseModel


class Tone(Enum):
    formal = "formal"
    casual = "casual"


class Language(Enum):
    french = "french"
    english = "english"
    spanish = "spanish"


class CoverLetterSchema(BaseModel):
    text: str
    tone: Tone
    language: Language


class CreateCoverLetterSchema(BaseModel):
    user_id: str
    resume_text: str
    job_text: str
    tone: Tone | None
    language: Language | None
