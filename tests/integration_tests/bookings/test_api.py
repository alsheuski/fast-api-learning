async def test_get_my_bookings(authenticated_ac):
    response = await authenticated_ac.get("/booking/me")

    assert response.status_code == 200

    my_bookings = response.json()
    assert isinstance(my_bookings, list)


async def test_add_booking(authenticated_ac, db):
    room_id = (await db.rooms.get_all())[0].id

    response = await authenticated_ac.post(
        "/booking",
        json={"room_id": room_id, "date_from": "2025-08-12", "date_to": "2025-08-22"},
    )

    assert response.status_code == 200

    res = response.json()
    assert isinstance(res, dict)
    assert res["status"] == "OK"
    assert "data" in res
