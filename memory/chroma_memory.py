try:
    import chromadb
    from chromadb.client import Client
except Exception:
    chromadb = None


class ChromaMemory:
    def __init__(self, collection_name="oceanic"):
        if chromadb is None:
            raise RuntimeError("chromadb package not available; install chromadb to use ChromaMemory")
        self.collection_name = collection_name
        self.client = None
        self.collection = None

    async def connect(self):
        # chromadb client is synchronous; we keep it simple
        self.client = Client()
        self.collection = self.client.create_collection(self.collection_name)

    async def store(self, kind, data):
        # store data as text
        txt = f"{kind}: {data}"
        self.collection.add(documents=[txt], ids=[str(hash(txt))])

    async def fetch_recent(self, limit=10):
        results = self.collection.get(limit=limit)
        return results

    async def close(self):
        return
