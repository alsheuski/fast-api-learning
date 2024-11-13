import uvicorn
from fastapi import FastAPI, Query, Body

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
]


@app.get("/hotels")
def get_hotels(title: str | None = Query(None, description="Hotel title")):
    if title:
        return [hotel for hotel in hotels if hotel["title"] == title]
    return hotels


@app.post("/hotels")
def create_hotel(title: str = Body(embed=True)):
    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1, "title": title})
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}")
def replace_hotel(hotel_id: int, title: str = Body(), name: str = Body()):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return {"status": "OK"}


@app.patch(
    "/hotels/{hotel_id}",
    summary="Partial update of some hotel details",
    description="Method can update title or name fields of exact hotel by hotel ID",
)
def update_hotel(
    hotel_id: int, title: str | None = Body(None), name: str | None = Body(None)
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title is not None:
                hotel["title"] = title
            if name is not None:
                hotel["name"] = name
            return {"status": "OK"}


@app.delete("/hotels/{id}")
def delete_hotel(id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != id]
    return {"status": "OK"}


@app.get("/")
def func():
    return "Hello, World!"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
