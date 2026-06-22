import os
import httpx


async def call_openai(prompt: str):
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200,
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(url, json=data, headers=headers)
        r.raise_for_status()
        j = r.json()
        return j
