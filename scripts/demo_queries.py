"""Demo script to show database queries in action."""

import asyncio
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sqlalchemy import select

from database import get_db
from services import db_service


async def demo_hospitals():
    """Demo: Get all hospitals."""
    print("\n" + "=" * 60)
    print("DEMO: List all hospitals")
    print("=" * 60)

    async with get_db() as session:
        result = await session.execute(
            select(
                db_service.orm_models.Hospital.id,
                db_service.orm_models.Hospital.name,
                db_service.orm_models.Hospital.city,
                db_service.orm_models.Hospital.phoneNumber,
            )
        )
        hospitals = result.all()

        for hospital in hospitals:
            print(f"\n[{hospital.id}] {hospital.name}")
            print(f"  City: {hospital.city}")
            print(f"  Phone: {hospital.phoneNumber or 'N/A'}")


async def demo_hospitals_by_city():
    """Demo: Get hospitals by city."""
    print("\n" + "=" * 60)
    print("DEMO: Get hospitals in a specific city")
    print("=" * 60)

    # Get unique cities first
    async with get_db() as session:
        result = await session.execute(
            select(db_service.orm_models.Hospital.city)
            .distinct()
            .where(db_service.orm_models.Hospital.city.isnot(None))
        )
        cities = [row[0] for row in result.all()]

    if not cities:
        print("No cities found")
        return

    city = cities[0]  # Use first city as example
    print(f"\nSearching for hospitals in: {city}")

    async with get_db() as session:
        hospitals = await db_service.get_hospitals_by_city(session, city)

        print(f"\nFound {len(hospitals)} hospital(s):")
        for hospital in hospitals:
            print(f"  - {hospital.name}")
            if hospital.address is not None:
                print(f"    Address: {hospital.address}")


async def demo_users():
    """Demo: List all users."""
    print("\n" + "=" * 60)
    print("DEMO: List all users")
    print("=" * 60)

    async with get_db() as session:
        result = await session.execute(
            select(
                db_service.orm_models.User.id,
                db_service.orm_models.User.firstname,
                db_service.orm_models.User.surname,
                db_service.orm_models.User.email,
            ).limit(5)
        )
        users = result.all()

        for user in users:
            print(f"\n[{user.id}]")
            print(f"  Name: {user.firstname} {user.surname}")
            print(f"  Email: {user.email}")


async def demo_hospital_status():
    """Demo: Get hospital status."""
    print("\n" + "=" * 60)
    print("DEMO: Hospital availability status")
    print("=" * 60)

    async with get_db() as session:
        # Get a hospital with status
        result = await session.execute(
            select(db_service.orm_models.HospitalStatus)
            .join(db_service.orm_models.Hospital)
            .limit(5)
        )
        statuses = result.scalars().all()

        if not statuses:
            print("\nNo hospital status data found")
            return

        for status in statuses:
            # Get hospital details
            hospital = await db_service.get_hospital_by_id(session, str(status.hospitalId))
            if hospital:
                print(f"\n{hospital.name}")
                print(f"  Available beds: {status.availableBeds or 0}")
                print(f"  ICU beds: {status.icuBeds or 0}")
                print(f"  Ventilators: {status.ventilators or 0}")


async def main():
    """Run all demos."""
    print("\n" + "=" * 60)
    print("NeonDB Database Demo")
    print("=" * 60)

    try:
        await demo_hospitals()
        await demo_hospitals_by_city()
        await demo_users()
        await demo_hospital_status()

        print("\n" + "=" * 60)
        print("Demo completed successfully!")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\n[ERROR] Demo failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
