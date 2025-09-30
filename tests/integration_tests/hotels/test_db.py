from src.schemas.hotels import HotelAdd


async def test_add_hotel(db):
    hotel_data = HotelAdd(title="Hotel 5 start", location="Sochi")

    await db.hotels.create(hotel_data)
    await db.commit()
