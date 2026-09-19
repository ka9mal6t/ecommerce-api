from pydantic import BaseModel


class SProduct(BaseModel):
    name: str
    description: str
    price: float
    image_url: str


