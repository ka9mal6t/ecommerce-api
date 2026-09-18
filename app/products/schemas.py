from pydantic import BaseModel, EmailStr


class SProduct(BaseModel):
    name: str
    description: str
    price = float
    image_url: str


