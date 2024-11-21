from src.repos.base import BaseRepository
from src.models.bookings import BookinsOrm
from src.schemas.bookings import Booking


class BookingRepository(BaseRepository):
    model = BookinsOrm
    schema = Booking
