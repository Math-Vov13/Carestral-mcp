"""Carestral MCP Server - Main server implementation."""

import asyncio
import datetime
import json
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, TextContent, Tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Healthcare knowledge base for symptom assessment
SYMPTOM_DATABASE = {
    "fever": {
        "severity": "moderate",
        "urgent": False,
        "specialties": ["general_practice", "internal_medicine"],
        "description": "Elevated body temperature above normal range (>38°C/100.4°F)",
        "red_flags": ["fever >40°C", "fever lasting >3 days", "accompanied by confusion"],
    },
    "chest_pain": {
        "severity": "high",
        "urgent": True,
        "specialties": ["cardiology", "emergency_medicine"],
        "description": "Pain or discomfort in the chest area",
        "red_flags": ["crushing pain", "radiating to arm/jaw", "shortness of breath"],
    },
    "headache": {
        "severity": "low",
        "urgent": False,
        "specialties": ["general_practice", "neurology"],
        "description": "Pain in the head or upper neck region",
        "red_flags": ["sudden severe headache", "with vision changes", "with fever and stiff neck"],
    },
    "cough": {
        "severity": "low",
        "urgent": False,
        "specialties": ["general_practice", "pulmonology"],
        "description": "Sudden expulsion of air from the lungs",
        "red_flags": ["coughing blood", "difficulty breathing", "lasting >3 weeks"],
    },
    "abdominal_pain": {
        "severity": "moderate",
        "urgent": False,
        "specialties": ["general_practice", "gastroenterology"],
        "description": "Pain in the stomach or belly area",
        "red_flags": ["severe pain", "with vomiting blood", "rigid abdomen"],
    },
}

SPECIALTIES = {
    "general_practice": {
        "name": "General Practice",
        "description": "Primary care for common health issues",
        "wait_time": "1-3 days",
    },
    "emergency_medicine": {
        "name": "Emergency Medicine",
        "description": "Immediate care for urgent conditions",
        "wait_time": "immediate",
    },
    "cardiology": {
        "name": "Cardiology",
        "description": "Heart and cardiovascular system care",
        "wait_time": "1-2 weeks",
    },
    "neurology": {
        "name": "Neurology",
        "description": "Brain and nervous system care",
        "wait_time": "2-4 weeks",
    },
    "pulmonology": {
        "name": "Pulmonology",
        "description": "Lung and respiratory system care",
        "wait_time": "1-2 weeks",
    },
    "gastroenterology": {
        "name": "Gastroenterology",
        "description": "Digestive system care",
        "wait_time": "1-3 weeks",
    },
    "internal_medicine": {
        "name": "Internal Medicine",
        "description": "Adult disease prevention and treatment",
        "wait_time": "3-7 days",
    },
}

# Initialize MCP server
app = Server("carestral-mcp")


@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available healthcare resources."""
    return [
        Resource(
            uri="carestral://symptoms/database",
            name="Symptom Database",
            mimeType="application/json",
            description="Database of common symptoms and their characteristics",
        ),
        Resource(
            uri="carestral://specialties/list",
            name="Medical Specialties",
            mimeType="application/json",
            description="List of available medical specialties and their information",
        ),
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read healthcare resource content."""
    if uri == "carestral://symptoms/database":
        return json.dumps(SYMPTOM_DATABASE, indent=2)
    elif uri == "carestral://specialties/list":
        return json.dumps(SPECIALTIES, indent=2)
    else:
        available = ["carestral://symptoms/database", "carestral://specialties/list"]
        raise ValueError(f"Unknown resource: {uri}. Available resources: {available}")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available healthcare tools."""
    return [
        Tool(
            name="assess_symptoms",
            description="Assess patient symptoms and provide severity level and recommendations",
            inputSchema={
                "type": "object",
                "properties": {
                    "symptoms": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of symptoms the patient is experiencing",
                    },
                    "duration": {
                        "type": "string",
                        "description": (
                            "How long symptoms have been present (e.g., '2 days', '1 week')"
                        ),
                    },
                    "severity": {
                        "type": "string",
                        "enum": ["mild", "moderate", "severe"],
                        "description": "Patient's subjective severity rating",
                    },
                },
                "required": ["symptoms"],
            },
        ),
        Tool(
            name="find_specialist",
            description="Find appropriate medical specialist based on symptoms or condition",
            inputSchema={
                "type": "object",
                "properties": {
                    "condition": {
                        "type": "string",
                        "description": "Medical condition or primary symptom",
                    },
                    "urgency": {
                        "type": "string",
                        "enum": ["routine", "urgent", "emergency"],
                        "description": "Level of urgency for care",
                    },
                },
                "required": ["condition"],
            },
        ),
        Tool(
            name="create_referral",
            description="Create a referral to connect patient with appropriate healthcare provider",
            inputSchema={
                "type": "object",
                "properties": {
                    "patient_id": {
                        "type": "string",
                        "description": "Patient identifier",
                    },
                    "specialty": {
                        "type": "string",
                        "description": "Medical specialty for referral",
                    },
                    "symptoms": {
                        "type": "string",
                        "description": "Summary of patient symptoms",
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["routine", "urgent", "stat"],
                        "description": "Priority level for referral",
                    },
                },
                "required": ["patient_id", "specialty", "symptoms"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Execute healthcare tools."""
    if not isinstance(arguments, dict):
        return [TextContent(
            type="text",
            text=f"Error: Invalid arguments type. Expected dict, got {type(arguments).__name__}"
        )]

    if name == "assess_symptoms":
        return await assess_symptoms(arguments)
    elif name == "find_specialist":
        return await find_specialist(arguments)
    elif name == "create_referral":
        return await create_referral(arguments)
    else:
        available = ["assess_symptoms", "find_specialist", "create_referral"]
        raise ValueError(f"Unknown tool: {name}. Available tools: {available}")


async def assess_symptoms(arguments: dict) -> list[TextContent]:
    """Assess patient symptoms and provide recommendations."""
    symptoms = arguments.get("symptoms", [])
    duration = arguments.get("duration", "unknown")
    patient_severity = arguments.get("severity", "moderate")

    if not symptoms:
        return [TextContent(
            type="text",
            text="No symptoms provided for assessment."
        )]

    # Analyze symptoms
    assessment = {
        "symptoms_analyzed": [],
        "max_severity": "low",
        "requires_urgent_care": False,
        "recommended_specialties": set(),
        "red_flags": [],
    }

    for symptom in symptoms:
        symptom_lower = symptom.lower().replace(" ", "_")
        if symptom_lower in SYMPTOM_DATABASE:
            symptom_info = SYMPTOM_DATABASE[symptom_lower]
            assessment["symptoms_analyzed"].append({
                "symptom": symptom,
                "info": symptom_info
            })

            # Update max severity
            severity_order = ["low", "moderate", "high"]
            current_severity_idx = severity_order.index(symptom_info["severity"])
            max_severity_idx = severity_order.index(assessment["max_severity"])
            if current_severity_idx > max_severity_idx:
                assessment["max_severity"] = symptom_info["severity"]

            # Check if urgent
            if symptom_info["urgent"]:
                assessment["requires_urgent_care"] = True

            # Add specialties
            assessment["recommended_specialties"].update(symptom_info["specialties"])

            # Add red flags
            assessment["red_flags"].extend(symptom_info["red_flags"])

    # Generate assessment report
    report = "**SYMPTOM ASSESSMENT REPORT**\n\n"
    report += f"**Symptoms Duration:** {duration}\n"
    report += f"**Patient-Reported Severity:** {patient_severity}\n"
    report += f"**Assessed Maximum Severity:** {assessment['max_severity']}\n"
    urgent_status = 'YES ⚠️' if assessment['requires_urgent_care'] else 'No'
    report += f"**Urgent Care Required:** {urgent_status}\n\n"

    if assessment["symptoms_analyzed"]:
        report += "**Symptoms Analyzed:**\n"
        for item in assessment["symptoms_analyzed"]:
            report += f"- {item['symptom']}: {item['info']['description']}\n"
        report += "\n"

    if assessment["red_flags"]:
        report += "**⚠️ Red Flags to Watch For:**\n"
        for flag in set(assessment["red_flags"]):
            report += f"- {flag}\n"
        report += "\n"

    if assessment["recommended_specialties"]:
        report += "**Recommended Medical Specialties:**\n"
        for specialty in assessment["recommended_specialties"]:
            if specialty in SPECIALTIES:
                spec_info = SPECIALTIES[specialty]
                report += f"- {spec_info['name']}: {spec_info['description']}\n"
                report += f"  Typical wait time: {spec_info['wait_time']}\n"
        report += "\n"

    if assessment["requires_urgent_care"]:
        report += (
            "**⚠️ RECOMMENDATION:** Seek immediate medical attention or "
            "visit emergency department.\n"
        )
    else:
        report += (
            "**RECOMMENDATION:** Schedule appointment with appropriate specialist. "
            "Monitor symptoms.\n"
        )

    return [TextContent(type="text", text=report)]


async def find_specialist(arguments: dict) -> list[TextContent]:
    """Find appropriate medical specialist."""
    condition = arguments.get("condition", "").lower().replace(" ", "_")
    urgency = arguments.get("urgency", "routine")

    # Try to match condition to symptom database
    matched_specialties = set()
    if condition in SYMPTOM_DATABASE:
        symptom_info = SYMPTOM_DATABASE[condition]
        matched_specialties.update(symptom_info["specialties"])

    # Generate report
    report = "**SPECIALIST FINDER REPORT**\n\n"
    report += f"**Condition:** {condition.replace('_', ' ').title()}\n"
    report += f"**Urgency Level:** {urgency}\n\n"

    if urgency == "emergency":
        report += "**⚠️ EMERGENCY:** Proceed to nearest emergency department immediately.\n\n"
        matched_specialties.add("emergency_medicine")

    if matched_specialties:
        report += "**Recommended Specialists:**\n"
        for specialty in matched_specialties:
            if specialty in SPECIALTIES:
                spec_info = SPECIALTIES[specialty]
                report += f"\n**{spec_info['name']}**\n"
                report += f"- {spec_info['description']}\n"
                report += f"- Typical wait time: {spec_info['wait_time']}\n"
    else:
        report += "**Recommendation:** Start with General Practice for initial evaluation.\n"
        if "general_practice" in SPECIALTIES:
            spec_info = SPECIALTIES["general_practice"]
            report += f"\n**{spec_info['name']}**\n"
            report += f"- {spec_info['description']}\n"
            report += f"- Typical wait time: {spec_info['wait_time']}\n"

    return [TextContent(type="text", text=report)]


async def create_referral(arguments: dict) -> list[TextContent]:
    """Create a patient referral."""
    patient_id = arguments.get("patient_id", "")
    specialty = arguments.get("specialty", "")
    symptoms = arguments.get("symptoms", "")
    priority = arguments.get("priority", "routine")

    # Generate referral document
    # Handle short patient IDs gracefully
    patient_id_suffix = patient_id[:8] if len(patient_id) >= 8 else patient_id.ljust(8, '0')
    referral_id = f"REF-{datetime.datetime.now().strftime('%Y%m%d')}-{patient_id_suffix}"

    report = "**MEDICAL REFERRAL CREATED**\n\n"
    report += f"**Referral ID:** {referral_id}\n"
    report += f"**Patient ID:** {patient_id}\n"
    report += f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    report += f"**Priority:** {priority.upper()}\n\n"

    report += f"**Referred to:** {specialty.replace('_', ' ').title()}\n"
    if specialty in SPECIALTIES:
        spec_info = SPECIALTIES[specialty]
        report += f"**Specialty Description:** {spec_info['description']}\n"
        report += f"**Expected Wait Time:** {spec_info['wait_time']}\n\n"

    report += f"**Symptoms Summary:**\n{symptoms}\n\n"

    if priority == "stat":
        report += "**⚠️ STAT PRIORITY:** This referral requires immediate attention.\n"
    elif priority == "urgent":
        report += "**⚠️ URGENT:** Please schedule within 24-48 hours.\n"
    else:
        report += "**STATUS:** Referral submitted. Patient will be contacted for scheduling.\n"

    report += "\n**Next Steps:**\n"
    report += "1. Patient will receive appointment confirmation via email/SMS\n"
    report += "2. Bring referral ID and medical records to appointment\n"
    report += "3. Contact provider if symptoms worsen before appointment\n"

    return [TextContent(type="text", text=report)]


@app.list_prompts()
async def list_prompts():
    """List available prompt templates."""
    from mcp.types import Prompt, PromptArgument

    return [
        Prompt(
            name="triage_patient",
            description="Triage a patient by assessing symptoms and recommending next steps",
            arguments=[
                PromptArgument(
                    name="symptoms",
                    description="Patient's reported symptoms",
                    required=True,
                ),
                PromptArgument(
                    name="duration",
                    description="How long symptoms have been present",
                    required=False,
                ),
            ],
        ),
        Prompt(
            name="referral_letter",
            description="Generate a medical referral letter",
            arguments=[
                PromptArgument(
                    name="patient_name",
                    description="Patient's name",
                    required=True,
                ),
                PromptArgument(
                    name="condition",
                    description="Medical condition requiring referral",
                    required=True,
                ),
                PromptArgument(
                    name="specialist",
                    description="Specialist type needed",
                    required=True,
                ),
            ],
        ),
    ]


@app.get_prompt()
async def get_prompt(name: str, arguments: dict | None) -> str:
    """Get a prompt template filled with arguments."""
    if name == "triage_patient":
        symptoms = arguments.get("symptoms", "") if arguments else ""
        duration = arguments.get("duration", "unknown") if arguments else "unknown"

        prompt = f"""You are a medical triage assistant. A patient has presented with the \
following information:

Symptoms: {symptoms}
Duration: {duration}

Please:
1. Use the assess_symptoms tool to analyze these symptoms
2. Determine the severity and urgency
3. Use the find_specialist tool if specialist care is needed
4. Provide clear, compassionate guidance on next steps

Remember to:
- Ask clarifying questions if needed
- Watch for red flag symptoms that require immediate care
- Provide reassurance while being thorough
- Explain your recommendations clearly
"""
        return prompt

    elif name == "referral_letter":
        patient_name = arguments.get("patient_name", "") if arguments else ""
        condition = arguments.get("condition", "") if arguments else ""
        specialist = arguments.get("specialist", "") if arguments else ""

        prompt = f"""You are drafting a medical referral letter. Please create a \
professional referral with:

Patient: {patient_name}
Condition: {condition}
Specialist Needed: {specialist}

Use the create_referral tool to generate the referral, then draft a formal letter including:
1. Reason for referral
2. Relevant symptoms and history
3. Urgency level
4. Any pertinent clinical findings

Keep the tone professional and include all necessary medical details.
"""
        return prompt

    else:
        available = ["triage_patient", "referral_letter"]
        raise ValueError(f"Unknown prompt: {name}. Available prompts: {available}")


async def main():
    """Run the Carestral MCP server."""
    logger.info("Starting Carestral MCP Server...")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
