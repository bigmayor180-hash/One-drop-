import os

def get_memory():
	backend = os.getenv("MEMORY_BACKEND", "sqlite").lower()
	if backend == "json":
		from .json_memory import JSONMemory

		return JSONMemory()
	elif backend == "chroma":
		from .chroma_memory import ChromaMemory

		return ChromaMemory()
	else:
		from .memory import Memory

		return Memory()

