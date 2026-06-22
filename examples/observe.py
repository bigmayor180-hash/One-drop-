"""
Example: Simple observation flow

This example shows how to use OceanicOS to observe data, store it in memory,
and retrieve recent observations.
"""

import asyncio
from kernel.drop import Drop


async def main():
    drop = Drop(name="SimpleObserver")
    await drop.boot()

    # Observe some data
    await drop.observe({"source": "sensor", "value": 42})
    await drop.observe({"source": "sensor", "value": 43})
    await drop.observe({"source": "user", "input": "hello drop"})

    # Remember and print recent observations
    recent = await drop.remember()
    print("Recent observations:")
    for row in recent:
        print(f"  {row}")

    await drop.memory.close()


if __name__ == "__main__":
    asyncio.run(main())
