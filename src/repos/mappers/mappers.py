from src.schemas.facilities import Facility
from src.models.facilities import FacilitiesOrm
from src.models.bookings import BookingsOrm
from src.schemas.bookings import Booking
from src.models.rooms import RoomsOrm
from src.repos.mappers.base import DataMapper
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room
from src.models.users import UsersOrm
from src.schemas.users import User


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomDatamapper(DataMapper):
    db_model = RoomsOrm
    schema = Room


class UserDatamapper(DataMapper):
    db_model = UsersOrm
    schema = User


class BookingDatamapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking


class FacilitiesDatamapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facility
