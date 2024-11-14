from fastapi import Body, Query, APIRouter
from sqlalchemy import insert, select

from models.hotels import HotelsOrm
from src.database import my_async_sessionmaker, engine
from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Hotel title"),
    location: str | None = Query(None),
):
    per_page = pagination.per_page or 5
    page = pagination.page or 1
    limit = pagination.per_page
    offset = per_page * (page - 1)

    async with my_async_sessionmaker() as session:
        query = select(HotelsOrm)

        if title:
            query = query.filter(HotelsOrm.title.icontains(title))

        if location:
            query = query.filter(HotelsOrm.location.icontains(location))

        query = query.limit(limit).offset(offset)

        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels


@router.post("")
async def create_hotel(
    hotel_data: Hotel = Body(
        openapi_examples={
            "1": {
                "summary": "Sochi",
                "value": {"title": "Sochi Hotel", "location": "sochi_hotel"},
            },
            "2": {
                "summary": "Dubai",
                "value": {"title": "Dubai Hotel", "location": "dubai_hotel"},
            },
        }
    ),
):
    async with my_async_sessionmaker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())

        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))

        await session.execute(add_hotel_stmt)
        await session.commit()

        return {"status": "OK"}


@router.put("/{hotel_id}")
def replace_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Partial update of some hotel details",
    description="Method can update title or name fields of exact hotel by hotel ID",
)
def update_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name
            return {"status": "OK"}


@router.delete("/{id}")
def delete_hotel(id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != id]
    return {"status": "OK"}
