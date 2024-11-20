from pydantic import BaseModel, Field


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class Room(RoomAdd):
    id: int


class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None


class RoomPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    hotel_id: int | None = None
    price: int | None = None
    quantity: int | None = None
