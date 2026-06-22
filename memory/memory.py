import aiosqlite


class Memory:
    def __init__(self, path="oceanic_memory.db"):
        self.path = path
        self._conn = None

    async def connect(self):
        self._conn = await aiosqlite.connect(self.path)
        await self._conn.execute(
            "CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, kind TEXT, data TEXT, ts DATETIME DEFAULT CURRENT_TIMESTAMP)"
        )
        await self._conn.commit()

    async def store(self, kind, data):
        await self._conn.execute("INSERT INTO events(kind, data) VALUES(?, ?)", (kind, str(data)))
        await self._conn.commit()

    async def fetch_recent(self, limit=10):
        cur = await self._conn.execute("SELECT id, kind, data, ts FROM events ORDER BY id DESC LIMIT ?", (limit,))
        rows = await cur.fetchall()
        return rows

    async def close(self):
        if self._conn:
            await self._conn.close()
