
import pytest
from fastmcp.client import Client, FastMCPTransport

MCP_URL = "http://localhost:8080"
TOKEN = "dev-alice-token"
GUEST_TOKEN = "dev-guest-token-null"

import pytest_asyncio


@pytest_asyncio.fixture
async def mcp_client():
    from src.server import mcp
    async with Client(FastMCPTransport(mcp)) as client:
        yield client
