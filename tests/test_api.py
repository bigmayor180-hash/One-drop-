import pytest
from httpx import AsyncClient, ASGITransport
from interfaces.api import app, _drop
import asyncio


@pytest.fixture
async def client():
    # Initialize the drop before tests
    await _drop.boot()
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    
    # Cleanup
    await _drop.memory.close()


@pytest.mark.anyio
async def test_status(client):
    r = await client.get("/status")
    assert r.status_code == 200
    j = r.json()
    assert "name" in j
    assert "memory_count" in j


@pytest.mark.anyio
async def test_observe(client):
    payload = {"source": "test", "payload": {"msg": "hello"}}
    r = await client.post("/observe", json=payload)
    assert r.status_code == 200
    j = r.json()
    assert j.get("ok") is True
