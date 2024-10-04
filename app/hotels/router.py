from app.hotels.schemas import SHotel
from fastapi import APIRouter
from fastapi.params import Depends, Query
from app.hotels.models import HotelsSearchArgs
from datetime import date,datetime
from app.hotels.dao import HotelDAO
router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)


@router.get("/hotels")
def get_hotels(search_args: HotelsSearchArgs = Depends()):
    return search_args


@router.get("")
async def get_hotels_by_location_and_time(
        location: str,
    )   -> list[SHotel]:
        hotels = await HotelDAO.find_all(location=location)
        return hotels