
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


@pytest.mark.asyncio
async def test_list_tools(mcp_client):
    tools = await mcp_client.list_tools()
    assert any(tool.name == "greet" for tool in tools)


@pytest.mark.asyncio
async def test_greet_tool(mcp_client):
    result = await mcp_client.call_tool("greet", {"name": "TestUser"})
    assert result.data == "Hello, TestUser!"
