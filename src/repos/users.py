from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select

from src.models.users import UsersOrm
from src.schemas.users import User, UserWithHashedPassword
from src.repos.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_user_with_hashed_password(self, email: EmailStr):
        if self.model:
            query = select(self.model).filter_by(email=email)
            result = await self.session.execute(query)
            obj = result.scalars().one()
            return UserWithHashedPassword.model_validate(obj, from_attributes=True)
