from datetime import date

from fastapi import APIRouter, Depends
from pydantic import TypeAdapter

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookings
from app.exeptions import RoomCannotBeBooked
from app.tasks.tasks import send_booking_conf_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/booking",
    tags=["Бронирование"]
)

@router.get("/get_bookings")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookings]:
    return await BookingDAO.find_all(user_id=user.id)

@router.post("/add_booking")
async def add_booking(room_id: int, date_from: date, date_to: date, user: Users = Depends(get_current_user)):
    booking = await BookingDAO.add(user_id=user.id, room_id=room_id, date_from=date_from, date_to=date_to)
    if not booking:
        raise RoomCannotBeBooked
    booking_dict = TypeAdapter(SBookings).validate_python(booking.__dict__).model_dump()
    send_booking_conf_email.delay(booking_dict, user.email)
    return booking_dict