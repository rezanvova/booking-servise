
from fastapi import APIRouter,Request
from fastapi.params import Depends
from fastapi.templating import Jinja2Templates

from app.hotels.router import get_hotels_by_location_and_time

router = APIRouter(
    prefix="/pages",
    tags=["Фронт"]
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/hotels")
async def get_hotel_page(request: Request, hotels=Depends(get_hotels_by_location_and_time)):
    return templates.TemplateResponse(name="hotels.html", context={"request": request, "hotels": hotels})