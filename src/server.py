"""Carestral MCP Server - Main server implementation."""

import logging

from fastmcp import FastMCP
from .auth import verifier

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize MCP server
mcp = FastMCP("carestral-mcp", auth=verifier)


@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"


if __name__ == "__main__":
    logger.info("Starting Carestral MCP Server...")
    mcp.run(transport="http", port=8000)
