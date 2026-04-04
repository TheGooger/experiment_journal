import pytest
from httpx import AsyncClient

from app.schemas.experiment import ExperimentCreate


pytestmark = pytest.mark.asyncio


async def test_create_experiment_api(async_client: AsyncClient, auth_headers):
    payload = {
        "experiment_number": "v260307",
        "performed_at": "2026-03-26",
        "is_completed": "True",
        "project": "Test project",
        "goal": "Test goal",
    }
    response = await async_client.post("/experiments/", headers=auth_headers, json=payload)
    
    assert response.status_code == 201
    
    data = response.json()

    assert data["experiment_number"] == "v260307"
    assert data["is_completed"] == True
    assert "id" in data


async def test_get_one_experiment_not_found_api(async_client: AsyncClient, auth_headers):
    response = await async_client.get("/experiments/NONEXISTENT", headers=auth_headers)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


async def test_update_experiment_api(async_client: AsyncClient, auth_headers):
    create_payload = {
        "experiment_number": "v260310",
        "performed_at": "2026-03-26",
        "is_completed": "True",
        "project": "Test project",
        "goal": "Test goal",
    }
    create_resp = await async_client.post("/experiments/", headers=auth_headers, json=create_payload)
    assert create_resp.status_code == 201
    created_id = create_resp.json()['id']

    update_payload = {"project": "New test project"}
    response = await async_client.patch("/experiments/v260310", headers=auth_headers, json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["project"] == "New test project"
    assert data["experiment_number"] == "v260310"

    assert data['id'] == created_id


async def test_delete_experiment_api(async_client: AsyncClient, auth_headers):
    create_payload = {
        "experiment_number": "v260312",
        "performed_at": "2026-03-26",
        "is_completed": "True",
        "project": "Test project",
        "goal": "To delete",
    }
    await async_client.post("/experiments/", headers=auth_headers, json=create_payload)

    delete_resp = await async_client.delete("/experiments/v260312", headers=auth_headers)
    assert delete_resp.status_code == 204
    
    get_resp = await async_client.get("/experiments/v260312", headers=auth_headers)
    assert get_resp.status_code == 404
    