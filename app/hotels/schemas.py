
from pydantic import BaseModel


class SHotel(BaseModel):
        address: str
        name: str
        stars: int
