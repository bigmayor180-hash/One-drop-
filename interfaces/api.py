from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import asyncio
import os

from kernel.drop import Drop
from .auth import require_api_key

app = FastAPI(title="OceanicOS v2.1 Mirror Water Engine")
_drop = Drop(enable_agents=True, enable_mcp=True)


class Observation(BaseModel):
    source: str
    payload: dict


class Task(BaseModel):
    description: str
    priority: int = 1


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


# v2.1 — Mirror Water Engine Endpoints

@app.get("/v2/agents/pool")
async def agents_pool():
    """Get the agent pool status."""
    if not _drop.agents:
        return {"error": "Agent pool not enabled"}
    return await _drop.agents.health_check()


@app.post("/v2/agents/dispatch")
async def dispatch_agent(task: Task, _auth=Depends(require_api_key)):
    """Dispatch a task to an available agent."""
    if not _drop.agents:
        raise HTTPException(status_code=503, detail="Agent pool not available")
    result = await _drop.agents.dispatch(task.description)
    return {"ok": True, "result": result}


@app.post("/v2/agents/broadcast")
async def broadcast_agents(task: Task, _auth=Depends(require_api_key)):
    """Broadcast a task to all agents."""
    if not _drop.agents:
        raise HTTPException(status_code=503, detail="Agent pool not available")
    results = await _drop.agents.broadcast(task.description)
    return {"ok": True, "results": results}


@app.get("/v2/knowledge/graph")
async def knowledge_graph():
    """Get the knowledge graph structure."""
    if not _drop.knowledge_graph:
        return {"error": "Knowledge graph not available"}
    return {
        "nodes": len(_drop.knowledge_graph.nodes),
        "edges": len(_drop.knowledge_graph.edges),
        "nodes_data": list(_drop.knowledge_graph.nodes.values())[:10],
        "edges_data": _drop.knowledge_graph.edges[:10]
    }


@app.get("/v2/mcp/manifest")
async def mcp_manifest():
    """Get the MCP server manifest for integration."""
    if not _drop.mcp_server:
        return {"error": "MCP not enabled"}
    return _drop.mcp_server.get_manifest()


@app.get("/v2/version")
async def version():
    """Get Drop version and capabilities."""
    return {
        "name": _drop.name,
        "version": _drop.version,
        "capabilities": {
            "agents": _drop.agents is not None,
            "knowledge_graph": _drop.knowledge_graph is not None,
            "mcp": _drop.mcp_server is not None,
            "memory_backend": type(_drop.memory).__name__
        }
    }

