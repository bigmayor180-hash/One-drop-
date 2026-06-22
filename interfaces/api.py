from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import asyncio
import os

from kernel.drop import Drop
from .auth import require_api_key

app = FastAPI(title="OceanicOS API")
_drop = Drop()


class Observation(BaseModel):
    source: str
    payload: dict


@app.on_event("startup")
async def startup():
    await _drop.boot()
    asyncio.create_task(_drop.run_loop())


# Serve static web UI if present
if os.path.isdir("web"):
    app.mount("/static", StaticFiles(directory="web"), name="web")


@app.get("/")
async def root():
    index_path = os.path.join("web", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"ok": True, "name": _drop.name}


@app.get("/status")
async def status():
    mem = await _drop.remember()
    return {"name": _drop.name, "memory_count": len(mem)}


@app.post("/observe")
async def observe(obs: Observation, _auth=Depends(require_api_key)):
    try:
        await _drop.observe({"source": obs.source, "payload": obs.payload})
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/learn")
async def learn(request: Request, _auth=Depends(require_api_key)):
    # lightweight model integration stub: uses OPENAI_API_KEY if present
    data = await request.json()
    prompt = data.get("prompt")
    if not prompt:
        raise HTTPException(status_code=400, detail="missing prompt")
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        return {"ok": False, "reason": "OPENAI_API_KEY not configured"}
    try:
        # lazy import to avoid hard dependency if not used
        from models.openai_adapter import call_openai

        resp = await call_openai(prompt)
        return {"ok": True, "result": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
