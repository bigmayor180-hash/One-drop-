import os

def get_memory():
	backend = os.getenv("MEMORY_BACKEND", "sqlite").lower()
	if backend == "json":
		from .json_memory import JSONMemory

		return JSONMemory()
	else:
		from .memory import Memory

		return Memory()

