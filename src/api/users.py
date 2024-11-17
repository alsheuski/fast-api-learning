from fastapi.routing import APIRouter
from passlib.context import CryptContext


from src.repos.users import UsersRepository
from src.database import my_async_sessionmaker
from src.schemas.users import UserAdd, UserRequestAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(data: UserRequestAdd):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)

    async with my_async_sessionmaker() as session:

        await UsersRepository(session).create(new_user_data)
        await session.commit()

        return {
            "status": "OK"
        }
