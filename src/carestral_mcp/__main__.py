#!/usr/bin/env python3
"""CLI entry point for Carestral MCP Server."""

import asyncio
import sys

from carestral_mcp.server import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
