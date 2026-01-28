"""Example MCP client configuration for Carestral."""

# Claude Desktop Configuration
# Add this to your Claude Desktop config file:
# - macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
# - Windows: %APPDATA%\Claude\claude_desktop_config.json

CLAUDE_DESKTOP_CONFIG = {
    "mcpServers": {
        "carestral": {
            "command": "python",
            "args": ["-m", "carestral_mcp.server"],
            "cwd": "/path/to/Carestral-mcp/src",
            "env": {}
        }
    }
}

# Alternative: Using uv
CLAUDE_DESKTOP_CONFIG_UV = {
    "mcpServers": {
        "carestral": {
            "command": "uv",
            "args": ["run", "python", "-m", "carestral_mcp.server"],
            "cwd": "/path/to/Carestral-mcp",
            "env": {}
        }
    }
}
