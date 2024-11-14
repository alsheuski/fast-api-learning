from fastapi import Body, Query, APIRouter
from schemas.hotels import Hotel

router = APIRouter(prefix="/hotels", tags=["Hotels"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("")
def get_hotels(
    title: str | None = Query(None, description="Hotel title"),
    page: int = 1,
    per_page: int = 3,
):
    if title:
        return [hotel for hotel in hotels if hotel["title"] == title]
    return hotels[(page - 1) * per_page : page * per_page]


@router.post("")
def create_hotel(
    hotel_data: Hotel = Body(
        openapi_examples={
            "1": {
                "summary": "Sochi",
                "value": {"title": "Sochi Hotel", "name": "sochi_hotel"},
            },
            "2": {
                "summary": "Dubai",
                "value": {"title": "Dubai Hotel", "name": "dubai_hotel"},
            },
        }
    ),
):
    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1, "title": hotel_data.title})
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
