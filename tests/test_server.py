"""Basic tests for Carestral MCP server."""


import os

import httpx
import pytest

MCP_URL = os.getenv("MCP_URL", "http://localhost:8080")
TOKEN = "dev-alice-token"
GUEST_TOKEN = "dev-guest-token-null"


@pytest.mark.asyncio
async def test_connect_with_token():
	async with httpx.AsyncClient() as client:
		headers = {"Authorization": f"Bearer {TOKEN}"}
		resp = await client.get(f"{MCP_URL}/v1/whoami", headers=headers)
		assert resp.status_code == 200
		data = resp.json()
		assert data["client_id"] == "alice@company.com"


@pytest.mark.asyncio
async def test_connect_without_token():
	async with httpx.AsyncClient() as client:
		resp = await client.get(f"{MCP_URL}/v1/whoami")
		assert resp.status_code in (401, 403)


@pytest.mark.asyncio
async def test_tools_list():
	async with httpx.AsyncClient() as client:
		headers = {"Authorization": f"Bearer {TOKEN}"}
		resp = await client.get(f"{MCP_URL}/v1/tools", headers=headers)
		assert resp.status_code == 200
		data = resp.json()
		assert isinstance(data, list)
		assert any(tool["name"] == "greet" for tool in data)


@pytest.mark.asyncio
async def test_prompts_list():
	async with httpx.AsyncClient() as client:
		headers = {"Authorization": f"Bearer {TOKEN}"}
		resp = await client.get(f"{MCP_URL}/v1/prompts", headers=headers)
		assert resp.status_code == 200
		data = resp.json()
		assert isinstance(data, list)


@pytest.mark.asyncio
async def test_resources_list():
	async with httpx.AsyncClient() as client:
		headers = {"Authorization": f"Bearer {TOKEN}"}
		resp = await client.get(f"{MCP_URL}/v1/resources", headers=headers)
		assert resp.status_code == 200
		data = resp.json()
		assert isinstance(data, list)

