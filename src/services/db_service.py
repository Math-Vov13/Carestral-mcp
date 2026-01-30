"""Database service layer for handling database operations."""

from typing import List, Optional

from sqlalchemy import select
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


async def get_hospitals_by_city(session: AsyncSession, city: str) -> List[orm_models.Hospital]:
    """Get hospitals by city."""
    result = await session.execute(
        select(orm_models.Hospital).where(orm_models.Hospital.city == city)
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
    """Get hospital by name (case-insensitive)."""
    result = await session.execute(
        select(orm_models.Hospital).where(orm_models.Hospital.name.ilike(f"%{hospital_name}%"))
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
    patient_id: str,
    date: str,
    time: str,
    description: str | None = None,
) -> orm_models.Appointment:
    """Create a new appointment."""
    import uuid

    appointment = orm_models.Appointment(
        id=str(uuid.uuid4()),
        userId=user_id,
        hospitalId=hospital_id,
        patientId=patient_id,
        date=date,
        time=time,
        description=description,
        status="scheduled",
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
