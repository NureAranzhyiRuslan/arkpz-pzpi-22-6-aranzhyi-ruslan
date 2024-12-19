import pytest
from httpx import AsyncClient

from idk.models import UserRole, City, User
from tests.conftest import create_token, BCRYPT_HASH_123456789

TEST_CITY_LAT = 42.24
TEST_CITY_LONG = 24.42


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient):
    token = await create_token(UserRole.ADMIN)
    user = await User.create(first_name="1", last_name="2", email="1@example.com", password=BCRYPT_HASH_123456789)

    response = await client.get("/admin/users", headers={"authorization": token})
    assert response.status_code == 200, response.json()
    assert response.json()["count"] == 2
    assert len(response.json()["result"]) == 2

    response = await client.get(f"/admin/users/{user.id}", headers={"authorization": token})
    assert response.status_code == 200, response.json()
    assert response.json()["email"] == user.email

    response = await client.get(f"/admin/users/{user.id+100}", headers={"authorization": token})
    assert response.status_code == 404, response.json()


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient):
    token = await create_token(UserRole.ADMIN)
    user = await User.create(first_name="1", last_name="2", email="1@example.com", password=BCRYPT_HASH_123456789)

    response = await client.get(f"/admin/users/{user.id}", headers={"authorization": token})
    assert response.status_code == 200, response.json()

    response = await client.delete(f"/admin/users/{user.id}", headers={"authorization": token})
    assert response.status_code == 204, response.json()

    response = await client.get(f"/admin/users/{user.id}", headers={"authorization": token})
    assert response.status_code == 404, response.json()
