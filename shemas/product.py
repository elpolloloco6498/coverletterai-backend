from pydantic import BaseModel


class CheckoutMetadataSchema(BaseModel):
    product_id: str
    user_id: str
