"""Carestral MCP Server - Main server implementation."""

import logging

from fastmcp import Context, FastMCP

from auth import verifier

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize MCP server
mcp = FastMCP("mcp-carestral", auth=verifier)


@mcp.tool
async def greet(name: str) -> str:
    return f"Hello, {name}!"

@mcp.tool
async def get_profile(ctx: Context) -> dict:
    """Fetch user profile data. Like name and claims token data."""
    from fastmcp.server.dependencies import get_access_token

    token = get_access_token()
    logger.info(f"Access token for user: {token}")
    return {"name": token.client_id, "claims": token.claims}

if __name__ == "__main__":
    logger.info("Starting Carestral MCP Server...")
    mcp.run(transport="http", port=8080)
