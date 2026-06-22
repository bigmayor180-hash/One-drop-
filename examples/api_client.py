"""
Example: API client flow

This example shows how to interact with the OceanicOS API from a client.
Run the server first: `python drop.py`
Then run this: `python examples/api_client.py`
"""

import httpx
import asyncio
import json


async def main():
    base_url = "http://localhost:8000"
    api_key = "demo-key"  # Set OCEANIC_API_KEY=demo-key on server if auth is enabled

    async with httpx.AsyncClient() as client:
        # Check status
        print("🌊 Checking status...")
        res = await client.get(f"{base_url}/status")
        print(f"Status: {res.json()}")

        # Send observations
        print("\n🔍 Sending observations...")
        for i in range(3):
            payload = {"source": "api_client", "index": i, "msg": f"observation {i}"}
            headers = {}
            if api_key:
                headers["X-API-Key"] = api_key

            res = await client.post(
                f"{base_url}/observe",
                json={"source": "api_client", "payload": payload},
                headers=headers,
            )
            print(f"Observe {i}: {res.json()}")

        # Check status again
        print("\n🌊 Checking status after observations...")
        res = await client.get(f"{base_url}/status")
        print(f"Updated status: {res.json()}")


if __name__ == "__main__":
    asyncio.run(main())
