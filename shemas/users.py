from typing import List

from pydantic import BaseModel

from shemas.letters import LetterSchema
from shemas.resumes import ResumeSchema


class CreateUserSchema(BaseModel):
    id: str
    name: str
    email: str
    credits: int


class UserSchema(CreateUserSchema):
    letters: List[LetterSchema]
    resumes: List[ResumeSchema]
