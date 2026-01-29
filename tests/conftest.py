"""Pytest configuration and shared fixtures for all tests."""

import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_event_loop_policy():
    """Set event loop policy for Windows compatibility."""
    import asyncio
    import sys

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
