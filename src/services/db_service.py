"""Database service layer for handling database operations."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import orm_models


async def get_user_by_id(session: AsyncSession, user_id: str) -> Optional[orm_models.User]:
    """Get user by ID."""
    result = await session.execute(
        select(orm_models.User).where(orm_models.User.id == user_id)
    )
    return result.scalar_one_or_none()


async def get_user_by_email(session: AsyncSession, email: str) -> Optional[orm_models.User]:
    """Get user by email."""
    result = await session.execute(
        select(orm_models.User).where(orm_models.User.email == email)
    )
    return result.scalar_one_or_none()


async def get_all_hospitals(session: AsyncSession) -> List[orm_models.Hospital]:
    """Get all hospitals."""
    result = await session.execute(select(orm_models.Hospital))
    return list(result.scalars().all())


async def get_hospitals_by_city(session: AsyncSession, city: str) -> List[orm_models.Hospital]:
    """Get hospitals by city (fuzzy match using levenshtein)."""
    distance = func.levenshtein(func.lower(orm_models.Hospital.city), func.lower(city))
    result = await session.execute(
        select(orm_models.Hospital)
        .where(distance <= 5)
        .order_by(distance)
    )
    return list(result.scalars().all())


async def get_hospital_by_id(session: AsyncSession, hospital_id: str
                             ) -> Optional[orm_models.Hospital]:
    """Get hospital by ID."""
    result = await session.execute(
        select(orm_models.Hospital).where(orm_models.Hospital.id == hospital_id)
    )
    return result.scalar_one_or_none()


async def get_hospital_by_name(session: AsyncSession, hospital_name: str
                                ) -> Optional[orm_models.Hospital]:
    """Get closest hospital by name (fuzzy match using levenshtein)."""
    distance = func.levenshtein(func.lower(orm_models.Hospital.name), func.lower(hospital_name))
    result = await session.execute(
        select(orm_models.Hospital)
        .where(distance <= 10)
        .order_by(distance)
        .limit(1)
    )
    return result.scalar_one_or_none()


async def get_hospital_status(
    session: AsyncSession, hospital_id: str
) -> Optional[orm_models.HospitalStatus]:
    """Get the latest hospital status."""
    result = await session.execute(
        select(orm_models.HospitalStatus)
        .where(orm_models.HospitalStatus.hospitalId == hospital_id)
        .order_by(orm_models.HospitalStatus.createdAt.desc())
    )
    return result.scalar_one_or_none()


async def create_appointment(
    session: AsyncSession,
    user_id: str,
    hospital_id: str,
    appointment_date_time: datetime,
    description: str | None = None,
) -> orm_models.Appointment:
    """Create a new appointment."""
    import uuid

    # Strip timezone info to match TIMESTAMP WITHOUT TIME ZONE columns
    if appointment_date_time.tzinfo is not None:
        appointment_date_time = appointment_date_time.replace(tzinfo=None)

    appointment = orm_models.Appointment(
        id=str(uuid.uuid4()),
        userId=user_id,
        hospitalId=hospital_id,
        appointmentDateTime=appointment_date_time,
        description=description,
        status="pending",
    )
    session.add(appointment)
    await session.flush()
    return appointment


async def get_user_appointments(
    session: AsyncSession, user_id: str
) -> List[orm_models.Appointment]:
    """Get all appointments for a user."""
    result = await session.execute(
        select(orm_models.Appointment)
        .where(orm_models.Appointment.userId == user_id)
        .order_by(orm_models.Appointment.createdAt.desc())
    )
    return list(result.scalars().all())


async def get_appointment_by_id(
    session: AsyncSession, appointment_id: str
) -> Optional[orm_models.Appointment]:
    """Get appointment by ID."""
    result = await session.execute(
        select(orm_models.Appointment).where(orm_models.Appointment.id == appointment_id)
    )
    return result.scalar_one_or_none()
