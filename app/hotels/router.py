import asyncio
from fastapi_cache.decorator import cache
from pydantic import parse_obj_as
from app.hotels.schemas import SHotel
from fastapi import APIRouter
from fastapi.params import Depends
from app.hotels.models import HotelsSearchArgs
from app.hotels.dao import HotelDAO
router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)


@router.get("/hotels")
def get_hotels(search_args: HotelsSearchArgs = Depends()):
    return search_args

@router.get("", response_model=list[SHotel])
@cache(expire=20)
async def get_hotels_by_location_and_time(
        location: str,
        ) -> list[SHotel]:
        await asyncio.sleep(3)
        hotels = await HotelDAO.find_all(location=location)
        hotels_dict = [hotel.__dict__ for hotel in hotels]
        hotels_json = parse_obj_as(list[SHotel], hotels_dict)
        return hotels_json