from repos.mappers.mappers import BookingDatamapper
from src.repos.base import BaseRepository
from src.models.bookings import BookingsOrm


class BookingRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDatamapper
