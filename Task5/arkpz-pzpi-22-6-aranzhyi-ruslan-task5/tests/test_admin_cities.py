import pytest
from httpx import AsyncClient

from idk.models import UserRole, City
from tests.conftest import create_token

TEST_CITY_LAT = 42.24
TEST_CITY_LONG = 24.42


@pytest.mark.asyncio
async def test_create_city(client: AsyncClient):
    token_user = await create_token()
    token = await create_token(UserRole.ADMIN)

    response = await client.post("/admin/cities", headers={"authorization": token}, json={
        "name": "test",
        "latitude": TEST_CITY_LAT,
        "longitude": TEST_CITY_LONG,
    })
    assert response.status_code == 200, response.json()
    assert response.json()["name"] == "test"

    response = await client.post("/admin/cities", headers={"authorization": token_user}, json={
        "name": "test",
        "latitude": TEST_CITY_LAT,
        "longitude": TEST_CITY_LONG,
    })
    assert response.status_code == 403, response.json()

    response = await client.get("/admin/cities", headers={"authorization": token})
    assert response.status_code == 200, response.json()
    assert response.json()["count"] == 1
    assert len(response.json()["result"]) == 1


@pytest.mark.asyncio
async def test_get_city(client: AsyncClient):
    token = await create_token(UserRole.ADMIN)
    city = await City.create(name="test", latitude=TEST_CITY_LAT, longitude=TEST_CITY_LONG)

    response = await client.get(f"/admin/cities/{city.id}", headers={"authorization": token})
    assert response.status_code == 200, response.json()
    assert response.json()["name"] == city.name

    response = await client.get(f"/admin/cities/{city.id+100}", headers={"authorization": token})
    assert response.status_code == 404, response.json()


@pytest.mark.asyncio
async def test_edit_city(client: AsyncClient):
    token = await create_token(UserRole.ADMIN)
    city = await City.create(name="test", latitude=TEST_CITY_LAT, longitude=TEST_CITY_LONG)

    response = await client.patch(f"/admin/cities/{city.id}", headers={"authorization": token}, json={
        "name": "test_new",
    })
    assert response.status_code == 200, response.json()
    assert response.json()["name"] == "test_new"

    response = await client.get(f"/admin/cities/{city.id}", headers={"authorization": token})
    assert response.status_code == 200, response.json()
    assert response.json()["name"] == "test_new"

    response = await client.patch(f"/admin/cities/{city.id+100}", headers={"authorization": token}, json={
        "name": "test_new",
    })
    assert response.status_code == 404, response.json()


@pytest.mark.asyncio
async def test_delete_city(client: AsyncClient):
    token = await create_token(UserRole.ADMIN)
    city = await City.create(name="test", latitude=TEST_CITY_LAT, longitude=TEST_CITY_LONG)

    response = await client.get(f"/admin/cities/{city.id}", headers={"authorization": token})
    assert response.status_code == 200, response.json()

    response = await client.delete(f"/admin/cities/{city.id}", headers={"authorization": token})
    assert response.status_code == 204, response.json()

    response = await client.get(f"/admin/cities/{city.id}", headers={"authorization": token})
    assert response.status_code == 404, response.json()
