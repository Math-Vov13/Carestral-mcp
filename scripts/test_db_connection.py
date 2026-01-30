"""Test script to verify database connection and query data."""

import asyncio
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sqlalchemy import text

from database import engine, get_db


async def test_connection():
    """Test database connection."""
    print("Testing database connection...")

    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            print("[OK] Connected to PostgreSQL")
            print(f"  Version: {version}\n")
            return True
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return False


async def test_tables():
    """Test if tables exist."""
    print("Checking tables...")

    tables = [
        "User",
        "Hospital",
        "Appointment",
        "HospitalStatus",
        "MCP",
        "TempToken",
    ]

    try:
        async with engine.connect() as conn:
            for table in tables:
                result = await conn.execute(
                    text(
                        f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{
                            table}')"
                    )
                )
                exists = result.scalar()
                status = "[OK]" if exists else "[MISSING]"
                print(f"  {status} Table '{table}'")
            print()
            return True
    except Exception as e:
        print(f"[ERROR] Error checking tables: {e}\n")
        return False


async def test_queries():
    """Test basic queries."""
    print("Testing queries...")

    try:
        async with get_db() as session:
            # Test counting users
            result = await session.execute(text("SELECT COUNT(*) FROM \"User\""))
            user_count = result.scalar()
            print(f"  - Users in database: {user_count}")

            # Test counting hospitals
            result = await session.execute(text("SELECT COUNT(*) FROM \"Hospital\""))
            hospital_count = result.scalar()
            print(f"  - Hospitals in database: {hospital_count}")

            # Test counting appointments
            result = await session.execute(text("SELECT COUNT(*) FROM \"Appointment\""))
            appointment_count = result.scalar()
            print(f"  - Appointments in database: {appointment_count}")

            print("\n[OK] Queries executed successfully\n")
            return True
    except Exception as e:
        print(f"[ERROR] Query failed: {e}\n")
        return False


async def main():
    """Run all tests."""
    print("=" * 60)
    print("NeonDB Connection Test")
    print("=" * 60)
    print()

    # Test connection
    if not await test_connection():
        print("\n[WARNING] Cannot proceed without database connection")
        return

    # Test tables
    await test_tables()

    # Test queries
    await test_queries()

    print("=" * 60)
    print("Test completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
