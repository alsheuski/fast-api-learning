from datetime import date
from sqlalchemy import func, select

from src.models.rooms import RoomsOrm
from src.models.bookings import BookingsOrm
from src.repos.base import BaseRepository
from src.schemas.rooms import Room
from src.utils.helpers import print_sql


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        rooms_count = (
            select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
            .select_from(BookingsOrm)
            .filter(BookingsOrm.date_from <= date_to, BookingsOrm.date_to >= date_from)
            .group_by(BookingsOrm.room_id)
            .cte(name="rooms_count")
        )

        rooms_left_table = (
            select(
                RoomsOrm.id.label("room_id"),
                (
                    RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)
                ).label("rooms_left"),
            )
            .select_from(RoomsOrm)
            .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
            .cte(name="rooms_left_table")
        )

        rooms_ids_for_hotel = (
            select(RoomsOrm.id)
            .select_from(RoomsOrm)
            .filter_by(hotel_id=hotel_id)
            .subquery(name="rooms_ids_for_hotel")
        )

        query = (
            select(rooms_left_table)
            .select_from(rooms_left_table)
            .filter(
                rooms_left_table.c.rooms_left > 0,
                rooms_left_table.c.room_id.in_(rooms_ids_for_hotel),
            )
        )

        # print_sql(query)

        return await self.get_filtered(RoomsOrm.id.in_(query))
