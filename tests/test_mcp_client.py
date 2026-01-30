
import pytest
from fastmcp.client import Client, FastMCPTransport

MCP_URL = "http://localhost:8080"
TOKEN = "dev-alice-token"
GUEST_TOKEN = "dev-guest-token-null"

import pytest_asyncio


@pytest_asyncio.fixture
async def mcp_client():
    from server import mcp
    async with Client(FastMCPTransport(mcp)) as client:
        yield client


@pytest.mark.asyncio
async def test_list_tools(mcp_client):
    tools = await mcp_client.list_tools()
    assert any(tool.name == "list_hospitals" for tool in tools)
