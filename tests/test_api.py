import pytest
from httpx import AsyncClient
from interfaces.api import app


@pytest.mark.asyncio
async def test_status():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/status")
        assert r.status_code == 200
        j = r.json()
        assert "name" in j
        assert "memory_count" in j


@pytest.mark.asyncio
async def test_observe():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"source": "test", "payload": {"msg": "hello"}}
        r = await ac.post("/observe", json=payload)
        assert r.status_code == 200
        j = r.json()
        assert j.get("ok") is True
