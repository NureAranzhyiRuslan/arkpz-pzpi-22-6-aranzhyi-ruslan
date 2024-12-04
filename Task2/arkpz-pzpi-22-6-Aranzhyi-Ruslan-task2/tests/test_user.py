import pytest
from httpx import AsyncClient

from .conftest import create_token


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient):
    token = await create_token()

    response = await client.get("/user/info", headers={"authorization": token})
    assert response.status_code == 200, response.json()


@pytest.mark.asyncio
async def test_edit_user(client: AsyncClient):
    token = await create_token()

    response = await client.patch("/user/info", headers={"authorization": token}, json={
        "first_name": "test123"
    })
    assert response.status_code == 200, response.json()
    assert response.json()["first_name"] == "test123"
