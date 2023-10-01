from typing import List

from pydantic import BaseModel

from shemas.letters import LetterSchema


class CreateUserSchema(BaseModel):
    id: str
    name: str
    email: str
    credits: int


class UserSchema(CreateUserSchema):
    letters: List[LetterSchema]
