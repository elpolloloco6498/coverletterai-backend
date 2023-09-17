from pydantic import BaseModel


class ProductSchema(BaseModel):
    id: str
