"""Carestral MCP Server - Main server implementation."""

import logging
import random
from typing import List

from fastmcp import Context, FastMCP

from auth import verifier
from models.db_models import AppointmentRequest, Hospital, HospitalStatus, Patient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logging.getLogger("fastmcp.server.auth").setLevel(logging.DEBUG)



# Initialize MCP server
mcp = FastMCP("mcp-carestral", auth=verifier)


@mcp.tool
async def greet(name: str) -> str:
    return f"Hello, {name}!"

@mcp.tool
def getpatientdata(patient_id: str) -> Patient:
    """Fetch patient data from database"""

    # -------------------------------------------------------------------
    # - SQL query
    # - REST API call
    # -------------------------------------------------------------------

    db = {
        "P001": Patient(id="P001", name="Alice Martin", age=32, city="Paris"),
        "P002": Patient(id="P002", name="Jean Dupont", age=58, city="Lyon"),
    }
    # -------------------------------------------------------------------

    return db.get(patient_id)

@mcp.tool
def getnearhosp(city: str) -> List[Hospital]:
    """Return nearby hospitals for a given city"""

    # -------------------------------------------------------------------
    # - map service (?)
    # - Hospital registr API
    # - Map?

    hospitals = [
        Hospital(id="H001", name="Hôpital Saint-Louis", city="Paris", distance_km=2.1),
        Hospital(id="H002", name="Hôpital Lariboisière", city="Paris", distance_km=3.4),
        Hospital(id="H003", name="Hôpital Lyon Sud", city="Lyon", distance_km=4.0),
    ]
    # -------------------------------------------------------------------

    return [h for h in hospitals if h.city == city]

@mcp.tool
def gethospdata(hospital_id: str) -> Hospital:
    """Return hospital details"""

    # -------------------------------------------------------------------
    # info hopital / api
    # -------------------------------------------------------------------

    hospitals = {
        "H001": Hospital(id="H001", name="Hôpital Saint-Louis", city="Paris", distance_km=2.1),
        "H002": Hospital(id="H002", name="Hôpital Lariboisière", city="Paris", distance_km=3.4),
        "H003": Hospital(id="H003", name="Hôpital Lyon Sud", city="Lyon", distance_km=4.0),
    }
    # -------------------------------------------------------------------

    return hospitals[hospital_id]

@mcp.tool
def create_rdv(request: AppointmentRequest) -> str:
    """Create an appointment in hospital system"""

    # -------------------------------------------------------------------
    # hospital  database
    # - HL7/FHIR appointment creation request
    confirmation_id = f"RDV-{random.randint(1000,9999)}"
    return f"Appointment confirmed: {confirmation_id}"

@mcp.tool
def gethospdispo(hospital_id: str) -> HospitalStatus:
    """Return live hospital availability"""

    # -------------------------------------------------------------------
    # - Real-time hospital bed management system
    # - Emergency department queue API
    status = HospitalStatus(
        hospital_id=hospital_id,
        available_beds=random.randint(0, 20),
        waiting_time_min=random.randint(5, 120)
    )
    # -------------------------------------------------------------------

    return status

@mcp.tool
def assess_symptoms(symptoms: List[str], duration: str = None, severity: str = None) -> dict:
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
def create_referral(patient_id: str, specialist: str, reason: str, priority: str = None) -> dict:
    """Create a referral for a patient to see a specialist."""
    # -------------------------------------------------------------------
    # - Referral management system
    referral_id = f"REF-{random.randint(10000,99999)}"
    return {
        "referral_id": referral_id,
        "patient_id": patient_id,
        "specialist": specialist,
        "reason": reason,
        "priority": priority or "Normal",
        "status": "Created"
    }

@mcp.tool
def getappointment_status(appointment_id: str) -> dict:
    """Get the status of an appointment."""
    # -------------------------------------------------------------------
    # - tracking system
    status_options = ["Scheduled", "Completed", "Cancelled", "No-Show"]
    status = random.choice(status_options)
    return {
        "appointment_id": appointment_id,
        "status": status
    }






@mcp.tool
async def get_profile(ctx: Context) -> dict:
    """Fetch user profile data. Like name and claims token data."""
    from fastmcp.server.dependencies import get_access_token

    token = get_access_token()
    logger.info(f"Access token for user: {token}")
    return {"name": token.client_id, "claims": token.claims}

if __name__ == "__main__":
    logger.info("Starting Carestral MCP Server...")
    mcp.run(transport="http", port=8080)
