import pytest
from httpx import AsyncClient
from fastapi import FastAPI


@pytest.mark.anyio
async def test_health(client: AsyncClient, fastapi_app: FastAPI):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": True}


@pytest.mark.anyio
async def test_notes(client: AsyncClient, fastapi_app: FastAPI):
    response = await client.get("/api/v1/notes/")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.anyio
async def test_tenant_with_join(client: AsyncClient, fastapi_app: FastAPI):
    response = await client.get("/api/v1/tenant-with-join/")
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.anyio
async def test_tenant_with_auto_serializer(client: AsyncClient, fastapi_app: FastAPI):
    response = await client.get("/api/v1/tenant-with-auto-serializer/")
    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.anyio
async def test_admins(client: AsyncClient, fastapi_app: FastAPI):
    response = await client.get("/api/v1/admins/")
    assert response.status_code == 200
    assert len(response.json()) == 4


@pytest.mark.anyio
async def test_cache(client: AsyncClient, fastapi_app: FastAPI):
    response = await client.get("/api/v1/cache-test/")
    assert response.status_code == 200
    print(response.json())
