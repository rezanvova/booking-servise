from datetime import date

from sqlalchemy import select, and_, or_
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.sql.functions import count
from app.dao.base import BaseDAO
from app.bookings.models import Bookings
from app.database import engine, async_session_maker
from app.hotels.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(
            cls,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to: date,
    ):
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        ),
                    )
                )
            ).subquery()

            get_rooms_left = select(
                (Rooms.quantity - count(booked_rooms.c.room_id)).label("rooms_left")
            ).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id,isouter=True
            ).where(Rooms.id == room_id).group_by(
                Rooms.quantity
            )
            get_rooms_left = await session.execute(get_rooms_left)
            rooms_left :int =get_rooms_left.scalar()
            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price = price.scalar()
                add_booking = insert(Bookings).values(
                    room_id = room_id,
                    user_id = user_id,
                    date_from = date_from,
                    date_to = date_to,
                    price = price,
                ).returning(Bookings)
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
            else:
                return
