import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_success(async_client: AsyncClient):
    response = await async_client.post(
        "/auth/register",
        json={
            "user_name": "vova_test",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["user_name"] == "vova_test"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate(async_client: AsyncClient):
    payload = {
        "user_name": "vova_test_2",
        "password": "123456"
    }
    
    await async_client.post("/auth/register", json=payload)

    response = await async_client.post("/auth/register", json=payload)

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient):
    await async_client.post(
        "/auth/register",
        json={
            "user_name": "test_vova3",
            "password": "123456"
        }
    )

    response = await async_client.post(
        "/auth/login",
        data={
            "username": "test_vova3",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data


@pytest.mark.asyncio
async def test_login_wrong_password(async_client: AsyncClient):
    await async_client.post(
        "/auth/register",
        json={
            "user_name": "test_vova4",
            "password": "123456"
        }
    )

    response = await async_client.post(
        "/auth/login",
        data={
            "username": "test_vova3",
            "password": "wrong"
        }
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_protected_route(async_client: AsyncClient):
    # register
    await async_client.post(
        "/auth/register",
        json={
            "user_name": "test_vova4",
            "password": "123456"
        }
    )

    # login
    response = await async_client.post(
        "/auth/login",
        data={
            "username": "test_vova4",
            "password": "123456"
        }
    )

    assert response.status_code == 200
    token = response.json()["access_token"]

    # request with token
    response = await async_client.post(
        "/experiments/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "experiment_number": "vTEST",
            "performed_at": "2026-03-31",
            "is_completed": "True",
            "project": "Test project",
            "goal": "Test goal",
        }
    )

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_protected_route_no_token(async_client: AsyncClient):
    response = await async_client.post(
        "/experiments/",
        json={
            "experiment_number": "vTEST",
            "performed_at": "2026-03-31",
            "is_completed": "True",
            "project": "Test project",
            "goal": "Test goal",
        }
    )

    assert response.status_code == 401
