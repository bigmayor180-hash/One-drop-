#!/usr/bin/env python3
import asyncio
import uvicorn
from interfaces.api import app


def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    run_server()
