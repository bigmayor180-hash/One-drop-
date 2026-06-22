from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from kernel.drop import Drop

app = FastAPI(title="OceanicOS API")
_drop = Drop()


class Observation(BaseModel):
    source: str
    payload: dict


@app.on_event("startup")
async def startup():
    await _drop.boot()
    # start background loop
    asyncio.create_task(_drop.run_loop())


@app.get("/status")
async def status():
    mem = await _drop.remember()
    return {"name": _drop.name, "memory_count": len(mem)}


@app.post("/observe")
async def observe(obs: Observation):
    try:
        await _drop.observe({"source": obs.source, "payload": obs.payload})
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
