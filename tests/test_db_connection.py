"""Test script to verify database connection and query data."""

import sys

import pytest
from sqlalchemy import text

from src.database import get_db


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.skipif(sys.platform == "win32", reason="Event loop issues on Windows")
async def test_connection():
    """Test database connection."""
    async with get_db() as session:
        result = await session.execute(text("SELECT version()"))
        version = result.scalar()
        assert version is not None
        assert "PostgreSQL" in version


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.skipif(sys.platform == "win32", reason="Event loop issues on Windows")
async def test_tables():
    """Test if tables exist."""
    tables = [
        "User",
        "Hospital",
        "Appointment",
        "HospitalStatus",
        "MCP",
        "TempToken",
    ]

    async with get_db() as session:
        for table in tables:
            result = await session.execute(
                text(
                    f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table}')"
                )
            )
            exists = result.scalar()
            assert exists, f"Table '{table}' does not exist"


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.skipif(sys.platform == "win32", reason="Event loop issues on Windows")
async def test_queries():
    """Test basic queries."""
    async with get_db() as session:
        # Test counting users
        result = await session.execute(text("SELECT COUNT(*) FROM \"User\""))
        user_count = result.scalar()
        assert user_count is not None

        # Test counting hospitals
        result = await session.execute(text("SELECT COUNT(*) FROM \"Hospital\""))
        hospital_count = result.scalar()
        assert hospital_count is not None

        # Test counting appointments
        result = await session.execute(text("SELECT COUNT(*) FROM \"Appointment\""))
        appointment_count = result.scalar()
        assert appointment_count is not None
