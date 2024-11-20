from sqlalchemy import select

from src.schemas.rooms import Room
from src.models.rooms import RoomsOrm
from src.repos.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room
