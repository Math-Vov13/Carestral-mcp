"""Basic tests for Carestral MCP server."""

import pytest

from carestral_mcp.server import (
    SPECIALTIES,
    SYMPTOM_DATABASE,
    assess_symptoms,
    create_referral,
    find_specialist,
)


@pytest.mark.asyncio
async def test_assess_symptoms_basic():
    """Test basic symptom assessment."""
    arguments = {
        "symptoms": ["fever", "cough"],
        "duration": "2 days",
        "severity": "moderate"
    }

    result = await assess_symptoms(arguments)

    assert len(result) == 1
    assert result[0].type == "text"
    assert "SYMPTOM ASSESSMENT REPORT" in result[0].text
    assert "fever" in result[0].text.lower()
    assert "cough" in result[0].text.lower()


@pytest.mark.asyncio
async def test_assess_symptoms_urgent():
    """Test urgent symptom assessment."""
    arguments = {
        "symptoms": ["chest_pain"],
        "duration": "30 minutes",
        "severity": "severe"
    }

    result = await assess_symptoms(arguments)

    assert len(result) == 1
    assert "Urgent Care Required: YES" in result[0].text or "YES ⚠️" in result[0].text
    assert "cardiology" in result[0].text.lower()


@pytest.mark.asyncio
async def test_assess_symptoms_empty():
    """Test assessment with no symptoms."""
    arguments = {"symptoms": []}

    result = await assess_symptoms(arguments)

    assert len(result) == 1
    assert "No symptoms provided" in result[0].text


@pytest.mark.asyncio
async def test_find_specialist_condition():
    """Test finding specialist for a condition."""
    arguments = {
        "condition": "chest_pain",
        "urgency": "urgent"
    }

    result = await find_specialist(arguments)

    assert len(result) == 1
    assert "SPECIALIST FINDER REPORT" in result[0].text
    assert "cardiology" in result[0].text.lower() or "Cardiology" in result[0].text


@pytest.mark.asyncio
async def test_find_specialist_emergency():
    """Test emergency specialist finding."""
    arguments = {
        "condition": "severe_bleeding",
        "urgency": "emergency"
    }

    result = await find_specialist(arguments)

    assert len(result) == 1
    assert "EMERGENCY" in result[0].text
    assert "emergency" in result[0].text.lower()


@pytest.mark.asyncio
async def test_create_referral():
    """Test creating a medical referral."""
    arguments = {
        "patient_id": "P12345",
        "specialty": "cardiology",
        "symptoms": "Chest pain and shortness of breath",
        "priority": "urgent"
    }

    result = await create_referral(arguments)

    assert len(result) == 1
    assert "MEDICAL REFERRAL CREATED" in result[0].text
    assert "P12345" in result[0].text
    assert "cardiology" in result[0].text.lower() or "Cardiology" in result[0].text
    assert "REF-" in result[0].text


@pytest.mark.asyncio
async def test_create_referral_stat():
    """Test creating a STAT priority referral."""
    arguments = {
        "patient_id": "P99999",
        "specialty": "emergency_medicine",
        "symptoms": "Severe chest pain",
        "priority": "stat"
    }

    result = await create_referral(arguments)

    assert len(result) == 1
    assert "STAT" in result[0].text


def test_symptom_database_structure():
    """Test symptom database has required fields."""
    for symptom, info in SYMPTOM_DATABASE.items():
        assert "severity" in info
        assert "urgent" in info
        assert "specialties" in info
        assert "description" in info
        assert "red_flags" in info
        assert info["severity"] in ["low", "moderate", "high"]
        assert isinstance(info["urgent"], bool)
        assert isinstance(info["specialties"], list)


def test_specialties_structure():
    """Test specialties have required fields."""
    for specialty, info in SPECIALTIES.items():
        assert "name" in info
        assert "description" in info
        assert "wait_time" in info
        assert isinstance(info["name"], str)
        assert isinstance(info["description"], str)
        assert isinstance(info["wait_time"], str)
