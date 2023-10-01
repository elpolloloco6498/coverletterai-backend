import datetime

from pydantic import BaseModel


class CreateLetterSchema(BaseModel):
    company_name: str
    job_title: str
    language: str
    writing_style: str
    generation_date: datetime.date
    text: str


class LetterSchema(CreateLetterSchema):
    id: int
    user_id: str


class JobData(BaseModel):
    company_name: str
    job_title: str
