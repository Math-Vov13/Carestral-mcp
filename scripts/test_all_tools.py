"""Test script to verify all MCP tools work with NeonDB."""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from database import get_db
from services import db_service


async def test_get_patient_data():
    """Test getting patient/user data."""
    print("\n" + "=" * 60)
    print("TEST: Get Patient Data (from User table)")
    print("=" * 60)

    async with get_db() as session:
        from sqlalchemy import select

        from models import orm_models

        result = await session.execute(select(orm_models.User).limit(1))
        user = result.scalar_one_or_none()

        if user:
            print(f"\n[OK] Found user: {user.firstname} {user.surname}")
            print(f"  ID: {user.id}")
            print(f"  Email: {user.email}")
            print(f"  Age: {user.age}")
            return str(user.id)
        else:
            print("\n[WARNING] No users in database")
            return None


async def test_get_hospitals():
    """Test getting hospitals by city."""
    print("\n" + "=" * 60)
    print("TEST: Get Hospitals by City")
    print("=" * 60)

    async with get_db() as session:
        hospitals = await db_service.get_hospitals_by_city(session, "Paris")
        print(f"\n[OK] Found {len(hospitals)} hospitals in Paris")
        if hospitals:
            print(f"  Example: {hospitals[0].name}")
            return str(hospitals[0].id)
        return None


async def test_create_appointment(user_id: str, hospital_id: str):
    """Test creating an appointment."""
    print("\n" + "=" * 60)
    print("TEST: Create Appointment")
    print("=" * 60)

    async with get_db() as session:
        appointment = await db_service.create_appointment(
            session=session,
            user_id=user_id,
            hospital_id=hospital_id,
            appointment_date_time=datetime(2024, 2, 15, 14, 0),
            description="Test appointment",
        )

        print(f"\n[OK] Created appointment: {appointment.id}")
        print(f"  Status: {appointment.status}")
        print(f"  DateTime: {appointment.appointmentDateTime}")
        return str(appointment.id)


async def test_get_appointment_status(appointment_id: str):
    """Test getting appointment status."""
    print("\n" + "=" * 60)
    print("TEST: Get Appointment Status")
    print("=" * 60)

    async with get_db() as session:
        appointment = await db_service.get_appointment_by_id(session, appointment_id)

        if appointment:
            print(f"\n[OK] Found appointment: {appointment.id}")
            print(f"  Status: {appointment.status}")
            print(f"  DateTime: {appointment.appointmentDateTime}")
        else:
            print("\n[ERROR] Appointment not found")


async def test_get_hospital_status(hospital_id: str):
    """Test getting hospital availability."""
    print("\n" + "=" * 60)
    print("TEST: Get Hospital Status")
    print("=" * 60)

    async with get_db() as session:
        status = await db_service.get_hospital_status(session, hospital_id)

        if status:
            print("\n[OK] Hospital status:")
            print(f"  Available beds: {status.availableBeds}")
            print(f"  ICU beds: {status.icuBeds}")
            print(f"  Ventilators: {status.ventilators}")
        else:
            print("\n[WARNING] No status data for this hospital")


async def cleanup_test_appointment(appointment_id: str):
    """Delete test appointment."""
    print("\n" + "=" * 60)
    print("CLEANUP: Delete Test Appointment")
    print("=" * 60)

    async with get_db() as session:
        from models import orm_models

        result = await session.execute(
            select(orm_models.Appointment).where(
                orm_models.Appointment.id == appointment_id
            )
        )
        appointment = result.scalar_one_or_none()

        if appointment:
            await session.delete(appointment)
            await session.commit()
            print(f"\n[OK] Deleted test appointment: {appointment_id}")


async def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("MCP Tools Integration Test with NeonDB")
    print("=" * 60)

    try:
        user_id = await test_get_patient_data()

        if user_id is None:
            print("\n[ERROR] Cannot continue tests without user data")
            return

        hospital_id = await test_get_hospitals()

        if hospital_id is None:
            print("\n[ERROR] Cannot continue tests without hospital data")
            return

        appointment_id = await test_create_appointment(user_id, hospital_id)

        await test_get_appointment_status(appointment_id)

        await test_get_hospital_status(hospital_id)

        await cleanup_test_appointment(appointment_id)

        print("\n" + "=" * 60)
        print("All tests completed successfully!")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    from sqlalchemy import select

    asyncio.run(main())
