import json
import os
import asyncio


class JSONMemory:
    def __init__(self, path="oceanic_memory.json"):
        self.path = path
        # ensure file exists
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    async def connect(self):
        # no-op for file
        return

    async def store(self, kind, data):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._write, kind, data)

    def _write(self, kind, data):
        with open(self.path, "r+") as f:
            try:
                arr = json.load(f)
            except Exception:
                arr = []
            arr.append({"kind": kind, "data": data})
            f.seek(0)
            json.dump(arr, f, indent=2)
            f.truncate()

    async def fetch_recent(self, limit=10):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._read, limit)

    def _read(self, limit):
        with open(self.path, "r") as f:
            try:
                arr = json.load(f)
            except Exception:
                arr = []
        return list(reversed(arr))[:limit]

    async def close(self):
        return
