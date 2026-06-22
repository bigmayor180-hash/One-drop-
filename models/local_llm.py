import asyncio


async def generate(prompt: str, max_tokens: int = 128):
    """Stub for a local LLM adapter. Replace with real runner (ggml/llama.cpp bindings).

    Returns a fake echo response for now.
    """
    await asyncio.sleep(0.05)
    return {"model": "local-stub", "output": f"ECHO: {prompt[:200]}"}
