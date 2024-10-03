from fastapi import APIRouter
from fastapi.params import Depends
from app.hotels.models import HotelsSearchArgs

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)

@router.get("/hotels")
def get_hotels(search_args: HotelsSearchArgs = Depends()):
    return search_args