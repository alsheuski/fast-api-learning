from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String

from src.database import Base


class FacilitiesOrm(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(length=100))


class RoomsFacilitiesOrm(Base):
    __tablename__ = "rooms_facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    facilities_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))