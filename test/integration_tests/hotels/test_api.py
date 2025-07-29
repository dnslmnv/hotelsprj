

async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params= {
            "date_from" : "2024-01-01",
            "date_to" : "2024-01-03"
        }
    )
    print(f"response = {response.json()}")
    assert response.status_code == 200
