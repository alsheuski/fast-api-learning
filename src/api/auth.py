from fastapi import HTTPException, Response, Request
from fastapi.routing import APIRouter
from sqlalchemy import except_


from api.dependencies import UserIdDep
from src.repos.users import UsersRepository
from src.database import my_async_sessionmaker
from src.schemas.users import UserAdd, UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

auth = AuthService()


@router.post("/login")
async def login_user(data: UserRequestAdd, response: Response):
    async with my_async_sessionmaker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(
            email=data.email
        )

        if not user:
            return HTTPException(status_code=401, detail="User not found")

        if auth.verify_password(data.password, user.hashed_password):
            access_token = auth.create_access_token(
                {"user_id": user.id, "email": user.email}
            )
            response.set_cookie("access_token", access_token)
            return {"access_token": access_token}
        else:
            return HTTPException(status_code=422, detail="Bad request")


@router.post("/register")
async def register_user(data: UserRequestAdd):
    hashed_password = auth.hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)

    async with my_async_sessionmaker() as session:
        await UsersRepository(session).create(new_user_data)
        await session.commit()

        return {"status": "OK"}


@router.get("/me")
async def get_me(user_id: UserIdDep):
    async with my_async_sessionmaker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie('access_token')
    return {"status": "OK"}

