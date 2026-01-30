"""Carestral MCP Server - Main server implementation."""

import logging
import random
from typing import List

from fastmcp import Context, FastMCP
from fastmcp.server.dependencies import get_access_token

from auth import verifier
from database import get_db
from models.db_models import AppointmentRequest, Hospital, HospitalStatus
from services import db_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logging.getLogger("fastmcp.server.auth").setLevel(logging.DEBUG)
mcp = FastMCP("mcp-carestral", auth=verifier)


@mcp.tool
async def greet(name: str) -> str:
    return f"Hello, {name}!"

@mcp.tool
async def getnearhosp(city: str) -> List[Hospital]:
    """Return nearby hospitals for a given city"""

    # Fetch hospitals from database
    async with get_db() as session:
        db_hospitals = await db_service.get_hospitals_by_city(session, city)

        # Convert ORM models to Pydantic models
        hospitals = [
            Hospital(
                id=h.id,  # type: ignore[arg-type]
                name=h.name,  # type: ignore[arg-type]
                city=h.city or "",  # type: ignore[arg-type]
                distanceKm=h.distanceKm or 0.0,  # type: ignore[arg-type]
            )
            for h in db_hospitals
        ]

        return hospitals

@mcp.tool
async def gethospdata(hospital_id: str) -> Hospital:
    """Return hospital details"""

    # Fetch hospital from database
    async with get_db() as session:
        db_hospital = await db_service.get_hospital_by_id(session, hospital_id)

        if not db_hospital:
            raise ValueError(f"Hospital with ID {hospital_id} not found")

        return Hospital(
            id=db_hospital.id,  # type: ignore[arg-type]
            name=db_hospital.name,  # type: ignore[arg-type]
            city=db_hospital.city or "",  # type: ignore[arg-type]
            distanceKm=db_hospital.distanceKm or 0.0,  # type: ignore[arg-type]
        )

@mcp.tool
async def create_rdv(request: AppointmentRequest) -> str:
    """Create an appointment in hospital system"""

    token = get_access_token()
    if not token:
        raise ValueError("Not authenticated")

    patient_id = token.client_id

    async with get_db() as session:
        hospital_identifier = request.hospital_id
        hospital = await db_service.get_hospital_by_id(session, hospital_identifier)

        # If not found by ID, try to find by name
        if not hospital:
            hospital = await db_service.get_hospital_by_name(session, hospital_identifier)

        if not hospital:
            raise ValueError(f"Hospital with ID or name '{hospital_identifier}' not found")

        # Use the actual hospital ID from database
        resolved_hospital_id: str = str(hospital.id)

        appointment = await db_service.create_appointment(
            session=session,
            user_id=patient_id,
            hospital_id=resolved_hospital_id,
            patient_id=patient_id,
            date=request.date,
            time=request.time,
            description="Appointment created via MCP",
        )

        return f"Appointment confirmed: {appointment.id}"  # type: ignore[arg-type]

@mcp.tool
async def gethospdispo(hospital_id: str) -> HospitalStatus:
    """Return live hospital availability"""

    # Fetch hospital status from database
    async with get_db() as session:
        db_status = await db_service.get_hospital_status(session, hospital_id)

        if not db_status:
            # If no status exists, return default values
            return HospitalStatus(
                hospitalId=hospital_id,
                availableBeds=0,
                icuBeds=0,
                ventilators=0,
            )

        return HospitalStatus(
            hospitalId=db_status.hospitalId,  # type: ignore[arg-type]
            availableBeds=db_status.availableBeds or 0,  # type: ignore[arg-type]
            icuBeds=db_status.icuBeds or 0,  # type: ignore[arg-type]
            ventilators=db_status.ventilators or 0,  # type: ignore[arg-type]
        )

@mcp.tool
def assess_symptoms(
    symptoms: List[str], duration: str | None = None, severity: str | None = None
) -> dict:
    """Assess patient symptoms and provide severity levels and recommendations."""
    # -------------------------------------------------------------------
    # - Medical base
    # -assess algo
    assessment = {
        "symptoms": symptoms,
        "duration": duration,
        "severity": severity,
        "assessment": "Mild",
        "recommendation": "Rest and stay hydrated. Consult a doctor if symptoms persist."
    }
    # -------------------------------------------------------------------

    return assessment



@mcp.tool
def create_referral(
    specialist: str, reason: str, priority: str | None = None
) -> dict:
    """Create a referral for the authenticated patient to see a specialist."""
    token = get_access_token()
    if not token:
        raise ValueError("Not authenticated")

    # -------------------------------------------------------------------
    # - Referral management system
    referral_id = f"REF-{random.randint(10000,99999)}"
    return {
        "referral_id": referral_id,
        "patient_id": token.client_id,
        "specialist": specialist,
        "reason": reason,
        "priority": priority or "Normal",
        "status": "Created"
    }

@mcp.tool
async def getappointment_status(appointment_id: str) -> dict:
    """Get the status of an appointment owned by the authenticated user."""

    token = get_access_token()
    if not token:
        raise ValueError("Not authenticated")

    # Fetch appointment from database
    async with get_db() as session:
        appointment = await db_service.get_appointment_by_id(session, appointment_id)

        if not appointment:
            return {
                "appointment_id": appointment_id,
                "status": "Not Found",
                "error": "Appointment does not exist",
            }

        # Verify the appointment belongs to the authenticated user
        if str(appointment.userId) != token.client_id:
            return {
                "appointment_id": appointment_id,
                "status": "Access Denied",
                "error": "You do not have access to this appointment",
            }

        return {
            "appointment_id": appointment.id,  # type: ignore[dict-item]
            "status": appointment.status or "Unknown",  # type: ignore[dict-item]
            "date": appointment.date,  # type: ignore[dict-item]
            "time": appointment.time,  # type: ignore[dict-item]
            "hospital_id": appointment.hospitalId,  # type: ignore[dict-item]
        }


@mcp.tool
async def get_profile(ctx: Context) -> dict:
    """Fetch user profile data from database with token claims."""
    token = get_access_token()
    if not token:
        return {"error": "No access token found"}

    logger.info(f"Access token for user: {token}")

    # Try to get user from database by email (client_id is usually email)
    async with get_db() as session:
        user = await db_service.get_user_by_id(session, token.client_id)

        if user:
            return {
                "name": token.client_id,
                "claims": token.claims,
                "profile": {
                    "id": user.id,  # type: ignore[dict-item]
                    "firstname": user.firstname,  # type: ignore[dict-item]
                    "surname": user.surname,  # type: ignore[dict-item]
                    "email": user.email,  # type: ignore[dict-item]
                    "age": user.age,  # type: ignore[dict-item]
                    "phoneNumber": user.phoneNumber,  # type: ignore[dict-item]
                    "reservationCount": user.reservationCount,  # type: ignore[dict-item]
                },
            }
        else:
            # User not in database yet
            return {
                "name": token.client_id,
                "claims": token.claims,
                "profile": None,
                "message": "User authenticated but profile not found in database",
            }

if __name__ == "__main__":
    logger.info("Starting Carestral MCP Server...")
    mcp.run(transport="http", port=8080)
