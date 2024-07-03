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
    response = await client.get("/api/v1/students-list/")
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.anyio
async def test_tenant_with_auto_serializer(client: AsyncClient, fastapi_app: FastAPI):
    response = await client.get("/api/v1/student-with-auto-serializer/")
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.anyio
async def test_cache(client: AsyncClient, fastapi_app: FastAPI):
    response = await client.get("/api/v1/cache-test/")
    assert response.status_code == 200
    print(response.json())
