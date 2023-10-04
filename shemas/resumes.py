from pydantic import BaseModel


class ResumeSchema(BaseModel):
    id: int
    name: str
    text: str


class CreateResumeSchema(BaseModel):
    name: str
    text: str

