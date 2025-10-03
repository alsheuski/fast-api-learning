async def test_get_my_bookings(authenticated_ac):
    response = await authenticated_ac.get("/booking/me")

    assert response.status_code == 200

    my_bookings = response.json()
    assert isinstance(my_bookings, list)
