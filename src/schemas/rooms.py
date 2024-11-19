from pydantic import BaseModel, Field


class RoomAdd(BaseModel):
    hotel_id: int | None = Field(None)
    title: str
    description: str
    price: int
    quantity: int


class Room(RoomAdd):
    id: int


class RoomPATCH(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    hotel_id: int | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
