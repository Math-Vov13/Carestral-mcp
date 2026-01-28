# Carestral MCP

A Python-based Model Context Protocol (MCP) server for healthcare that connects doctors, hospitals, and patients worldwide. Provides AI-powered symptom pre-assessment and intelligent patient referral to appropriate medical services.

## Features

- 🏥 **Symptom Assessment**: Analyze patient symptoms with severity ratings and red flag detection
- 👨‍⚕️ **Specialist Finder**: Match patients with appropriate medical specialties based on their conditions
- 📋 **Smart Referrals**: Generate medical referrals with priority levels and specialist recommendations
- 🌐 **Healthcare Resources**: Access symptom databases and specialty information
- 💬 **Prompt Templates**: Pre-configured prompts for patient triage and referral letters

## Installation

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager

### Install from source

```bash
# Clone the repository
git clone https://github.com/Math-Vov13/Carestral-mcp.git
cd Carestral-mcp

# Install dependencies
pip install -e .
```

## Usage

### Running the MCP Server

Start the Carestral MCP server using stdio transport:

```bash
python -m carestral_mcp.server
```

Or directly:

```bash
python src/carestral_mcp/server.py
```

### MCP Client Configuration

Add to your MCP client configuration (e.g., Claude Desktop config):

```json
{
  "mcpServers": {
    "carestral": {
      "command": "python",
      "args": ["-m", "carestral_mcp.server"],
      "cwd": "/path/to/Carestral-mcp/src"
    }
  }
}
```

## Available Tools

### 1. assess_symptoms

Assess patient symptoms and provide severity levels and recommendations.

**Parameters:**
- `symptoms` (array, required): List of symptoms the patient is experiencing
- `duration` (string, optional): How long symptoms have been present
- `severity` (string, optional): Patient's subjective severity rating (mild/moderate/severe)

**Example:**
```json
{
  "symptoms": ["fever", "cough", "chest_pain"],
  "duration": "3 days",
  "severity": "moderate"
}
```

### 2. find_specialist

Find appropriate medical specialists based on symptoms or conditions.

**Parameters:**
- `condition` (string, required): Medical condition or primary symptom
- `urgency` (string, optional): Level of urgency (routine/urgent/emergency)

**Example:**
```json
{
  "condition": "chest_pain",
  "urgency": "urgent"
}
```

### 3. create_referral

Create a referral to connect patient with appropriate healthcare providers.

**Parameters:**
- `patient_id` (string, required): Patient identifier
- `specialty` (string, required): Medical specialty for referral
- `symptoms` (string, required): Summary of patient symptoms
- `priority` (string, optional): Priority level (routine/urgent/stat)

**Example:**
```json
{
  "patient_id": "P12345",
  "specialty": "cardiology",
  "symptoms": "Chest pain radiating to left arm, shortness of breath",
  "priority": "urgent"
}
```

## Available Resources

### carestral://symptoms/database

Comprehensive database of common symptoms with:
- Severity levels
- Urgency indicators
- Recommended specialties
- Red flag warnings

### carestral://specialties/list

Information about medical specialties including:
- Specialty descriptions
- Typical wait times
- Areas of expertise

## Prompt Templates

### triage_patient

Interactive patient triage workflow that assesses symptoms and recommends next steps.

**Arguments:**
- `symptoms`: Patient's reported symptoms
- `duration`: How long symptoms have been present

### referral_letter

Generate a professional medical referral letter.

**Arguments:**
- `patient_name`: Patient's name
- `condition`: Medical condition requiring referral
- `specialist`: Specialist type needed

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

### Code Quality

```bash
# Format and lint with ruff
ruff check .
ruff format .
```

## Healthcare Disclaimer

⚠️ **Important**: This MCP server is designed to assist healthcare professionals and provide preliminary assessments. It is **NOT** a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified healthcare providers with any questions regarding medical conditions.

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
