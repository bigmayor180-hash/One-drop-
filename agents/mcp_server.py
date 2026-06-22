"""
MCP Server: Model Context Protocol support for v2.1

Exposes OceanicOS via MCP so external tools can interact with it.
"""

import json
from typing import Any, Dict, List


class MCPServer:
    """Simple MCP protocol handler for Claude, Cursor, and other MCP clients."""

    def __init__(self, drop_instance):
        self.drop = drop_instance
        self.resources = []
        self.tools = []

    def register_resource(self, name: str, description: str, uri: str):
        """Register a resource available via MCP."""
        self.resources.append({
            "name": name,
            "description": description,
            "uri": uri
        })

    def register_tool(self, name: str, description: str, func):
        """Register a tool that can be called via MCP."""
        self.tools.append({
            "name": name,
            "description": description,
            "func": func
        })

    async def initialize(self):
        """Set up standard resources and tools."""
        # Resources
        self.register_resource(
            "memory",
            "Access to the Memory Ocean",
            "memory://events"
        )
        self.register_resource(
            "agents",
            "Pool of active agents",
            "agents://pool"
        )

        # Tools
        self.register_tool(
            "observe",
            "Send an observation to the Drop",
            self._tool_observe
        )
        self.register_tool(
            "query_memory",
            "Query the Memory Ocean",
            self._tool_query_memory
        )
        self.register_tool(
            "dispatch_agent",
            "Dispatch a task to an agent",
            self._tool_dispatch_agent
        )

    async def _tool_observe(self, source: str, payload: dict) -> dict:
        await self.drop.observe({"source": source, "payload": payload})
        return {"ok": True}

    async def _tool_query_memory(self, query: str, limit: int = 10) -> List:
        recent = await self.drop.remember()
        return recent[:limit]

    async def _tool_dispatch_agent(self, task: str) -> str:
        if hasattr(self.drop, 'agents') and self.drop.agents:
            return await self.drop.agents.dispatch(task)
        return "No agent pool available"

    def get_manifest(self) -> dict:
        """Return MCP manifest for client registration."""
        return {
            "name": "OceanicOS-v2.1",
            "version": "2.1.0",
            "resources": self.resources,
            "tools": [
                {
                    "name": t["name"],
                    "description": t["description"]
                }
                for t in self.tools
            ]
        }
