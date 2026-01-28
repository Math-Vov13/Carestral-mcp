"""Carestral MCP Server - Main server implementation."""

import logging

from fastmcp import Context, FastMCP

from auth import verifier

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize MCP server
mcp = FastMCP("mcp-carestral", auth=verifier)


@mcp.tool
async def greet(name: str) -> str:
    return f"Hello, {name}!"

@mcp.tool
def getPatientData(patient_id: str) -> Patient:
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
def getNearHosp(city: str) -> List[Hospital]:
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
def getHospData(hospital_id: str) -> Hospital:
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
def createRDV(request: AppointmentRequest) -> str:
    """Create an appointment in hospital system"""

    # -------------------------------------------------------------------
    # hospital  database
    # - HL7/FHIR appointment creation request
    confirmation_id = f"RDV-{random.randint(1000,9999)}"
    return f"Appointment confirmed: {confirmation_id}"

def getHospDispo(hospital_id: str) -> HospitalStatus:
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
async def get_profile(ctx: Context) -> dict:
    """Fetch user profile data. Like name and claims token data."""
    from fastmcp.server.dependencies import get_access_token

    token = get_access_token()
    logger.info(f"Access token for user: {token}")
    return {"name": token.client_id, "claims": token.claims}

if __name__ == "__main__":
    logger.info("Starting Carestral MCP Server...")
    mcp.run(transport="http", port=8080)
