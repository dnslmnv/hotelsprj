import pytest
from pytest import mark

from test.conftest import get_db_null_pool


@pytest.fixture(scope="module", autouse=False)
async def delete_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2024-01-01", "2024-01-03", 200),
    (1, "2024-01-01", "2024-01-03", 200),
    (1, "2024-01-01", "2024-01-03", 200),
    (1, "2024-01-01", "2024-01-03", 200),
    (1, "2024-01-01", "2024-01-03", 200),
    (1, "2024-01-01", "2024-01-03", 409),
])
async def test_add_booking(
        room_id, date_from, date_to, status_code,
        db, authenticated_ac
    ):
    # room_id = (await db.rooms.get_all())[0].id
    room_id = room_id
    response = await authenticated_ac.post(
        "/bookings",
        json = {
            "room_id" : room_id,
            "date_from" : date_from,
            "date_to" : date_to
        }
    )

    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert "data" in res


@pytest.mark.parametrize("room_id, date_from, date_to, status_code, bookings_amount", [
    (1, "2024-01-01", "2024-02-04", 200, 1),
    (1, "2024-02-01", "2024-03-03", 200, 2),
    (1, "2024-06-01", "2024-07-07", 200, 3),
])
async def test_add_and_get_my_bookings(
        room_id, date_from, date_to, status_code, bookings_amount, delete_bookings, authenticated_ac
    ):
    # room_id = (await db.rooms.get_all())[0].id
    room_id = room_id
    response = await authenticated_ac.post(
        "/bookings",
        json = {
            "room_id" : room_id,
            "date_from" : date_from,
            "date_to" : date_to
        }
    )

    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert "data" in res

    my_bookings_response = await authenticated_ac.get(
        "/bookings/me"
    )
    assert my_bookings_response.status_code == 200
    assert len(my_bookings_response.json()) == bookings_amount