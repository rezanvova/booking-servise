from sqlalchemy import JSON, Column, Integer, String , ForeignKey
from app.database import Base
from fastapi import Query
from typing import Optional
from datetime import date

class Hotels(Base):

    __tablename__ = "hotels"
    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    location = Column(String,nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(Integer,nullable=False)
    image_id = Column(Integer)

class Rooms(Base):

    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, nullable=False)
    hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    services = Column(JSON, nullable=True)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)


class HotelsSearchArgs():
    def __init__(
            self,
            location: str,
            date_from: date,
            date_to: date,
            has_spa: Optional[bool] = None,
            stars: Optional[int] = Query(None, ge=1, le=5)
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.has_spa = has_spa
        self.stars = stars


