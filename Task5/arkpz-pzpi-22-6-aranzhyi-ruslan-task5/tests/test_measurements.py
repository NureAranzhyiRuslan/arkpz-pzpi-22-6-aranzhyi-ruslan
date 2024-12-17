import pytest
from httpx import AsyncClient

from idk.models import City
from .conftest import create_token


@pytest.mark.asyncio
async def test_send_measurement(client: AsyncClient):
    token = await create_token()
    city = await City.create(name="test", latitude=42.24, longitude=24.42)

    response = await client.post("/sensors", headers={"authorization": token}, json={
        "city": city.id,
        "name": "test",
    })
    assert response.status_code == 200, response.json()
    api_key = response.json()["secret_key"]

    response = await client.post(f"/measurements", headers={"authorization": api_key}, json={
        "pressure": 123,
        "temperature": 456,
    })
    assert response.status_code == 204, response.json()


@pytest.mark.asyncio
async def test_get_measurements(client: AsyncClient):
    token = await create_token()
    city = await City.create(name="test", latitude=42.24, longitude=24.42)

    response = await client.post("/sensors", headers={"authorization": token}, json={
        "city": city.id,
        "name": "test",
    })
    assert response.status_code == 200, response.json()
    sensor_id = response.json()["id"]
    api_key = response.json()["secret_key"]

    response = await client.post(f"/measurements", headers={"authorization": api_key}, json={
        "pressure": 123,
        "temperature": 456,
    })
    assert response.status_code == 204, response.json()

    response = await client.get(f"/measurements/{sensor_id}", headers={"authorization": token})
    assert response.status_code == 200, response.json()
    assert len(response.json()) == 1
    assert response.json()[0]["pressure"] == 123
    assert response.json()[0]["temperature"] == 456
