from sqlalchemy import select

from models.users import UsersOrm
from schemas.users import User
from src.models.hotels import HotelsOrm
from src.repos.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User
