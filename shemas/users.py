from pydantic import BaseModel


class UserSchema(BaseModel):
    id: str
    name: str
    email: str
    credits: int
