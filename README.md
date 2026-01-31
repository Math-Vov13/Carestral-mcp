# Carestral MCP

A Python-based Model Context Protocol (MCP) server for healthcare that connects doctors, hospitals, and patients worldwide. Provides AI-powered symptom pre-assessment and intelligent patient referral to appropriate medical services.
- MCP standard introduced by Anthropic, view more [here](https://www.anthropic.com/news/model-context-protocol)
- MCP general developper docs for new work, view more [here](https://modelcontextprotocol.io/docs/getting-started/intro)

## Features

- 🏥 **Symptom Assessment**: Analyze patient symptoms with severity ratings and red flag detection
- 👨‍⚕️ **Specialist Finder**: Match patients with appropriate medical specialties based on their conditions
- 📋 **Smart Referrals**: Generate medical referrals with priority levels and specialist recommendations
- 🌐 **Healthcare Resources**: Access symptom databases and specialty information
- 💬 **Prompt Templates**: Pre-configured prompts for patient triage and referral letters
- 👤 **User Profile**: Connect user profile with AI for better understanding and the patient's medical history
- 📅 **Take rdvs**: Make an appointment with a specialist doctor to get treatment quickly

## URLs

- **HospiAI MCP**: mcp-carestral-app-349b535a.alpic.live/mcp
- **HospiAI Frontend**: hospi-ai-v8rf.vercel.app/
- **HospiAI frontend repo**: https://github.com/RayaneChCh-dev/HospiAI

## Technology

- Python
- FastMCP: Framework to build MCPs [docs here](https://fastmcp.wiki/en/getting-started/welcome)
- sqlalchemy: pgsql ORM [docs here](https://docs.sqlalchemy.org/en/20/intro.html)
- pytest: test your codebase [FastMCP tests](https://fastmcp.wiki/en/patterns/testing), [pytest docs](https://docs.pytest.org/en/stable/)
- ruff: python linter & formatter written in Rust [docs here](https://docs.astral.sh/ruff/)

## ⚡ Quick Start

### Prerequisites

- Python 3.10 or higher
- package manager: pip or uv (uv is recommended)

how to install [uv here](https://docs.astral.sh/uv/)

### Install from source

```bash
# Clone the repository
git clone https://github.com/Math-Vov13/Carestral-mcp.git
cd Carestral-mcp
```

### Config python env

```sh
# Copy .env and add your own variables!

cp .env.example .env
```

```env
## DATABASE
DATABASE_URL="<enter-your-pgsql-db-connection-url>"

## AUTH SETTINGS
AUTH_BASE_URL="<your-web-site-url>" ## (REMOVE THE END "/" FROM URL, e.g: 'hospi-ai-v8rf.vercel.app' and not 'hospi-ai-v8rf.vercel.app/')
```

```sh
# Create python venv
# with pip
python -m venv .venv

# or
# with uv (with uv you can skip the next step!)
uv venv
```

```sh
# Connect to python .venv
# with pip
.venv\Scripts\activate # (on windows)

# or

source .venv/bin/activate # (on macos/linux)
```

### Install project dependencies

```sh
# Install python deps
# with pip
pip install -r requirements.txt

# or
# with uv
uv sync
```

### Running the MCP Server

Start the Carestral MCP server using stdio transport:

```sh
# using fastmcp cli (https://fastmcp.wiki/en/patterns/cli)
# ⚠️ This will run your MCP on stdio mode
## see more: "https://modelcontextprotocol.io/docs/develop/connect-local-servers"

fastmcp run src/server.py
```

Or directly:

```bash
# ⚠️ This will run your MCP on http mode (RECOMMENDED)
# using python
python src/server.py

# or
# with uv
uv run src/server.py
```

### Connect a client to your MCP server

You can use your MCP with:
- **LMStudio**: https://lmstudio.ai/  [[USED BY ME FOR DEVELOPMENT TESTING WITH LOCAL AI AGENT]]
- **Claude Code/Desktop**
- **Cursor**
- **MistralAI**
- **ChatGPT**
- **custom project with AI**
- etc.

But first, you will need a valid auth token!

Add to your MCP client configuration (e.g., Claude Desktop config):

**Note:** Replace `/path/to/Carestral-mcp/src` with your actual installation path.

#### 1. STDIO mode
```json
{
  "mcpServers": {
    "hospiai": {
      "command": "python",
      "args": ["-m", "server"],
      "cwd": "/path/to/Carestral-mcp/src"
    }
  }
}
```

OR WITH UV

```json
{
  "mcpServers": {
    "hospiai": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/Carestral-mcp/src",
        "run",
        "server.py"
      ]
  }
}
```

#### 2. HTTP mode (RECOMMENDED)

```json
{
  "mcpServers": {
    "hospiai": {
      "url": "http://localhost:8080/mcp",
      "headers": {
        "Authorization": "Bearer <your-auth-token>"
      }
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

## Create your own Auth Web Site

See FastMCP docs for Token Verification [here](https://fastmcp.wiki/en/servers/auth/token-verification#jwks-endpoint-integration)

Steps:
- Generate a public key and private key on your frontend
- Add /.well-known/jwks.json endpoint
- Add token generation with private key on your frontend

You can acces our Web Site url here: https://hospi-ai-v8rf.vercel.app/dashboard/tokens

## Server Deployment

Actually, we are using Alpic MCP server (a french solution) [view more](https://alpic.ai/)
But you can use too:
- FastMCP Cloud [docs](https://horizon.prefect.io/)
- Heroku [docs](https://www.heroku.com/python/)
- AWS
- etc.

[FastMCP docs](https://fastmcp.wiki/en/deployment/running-server)

## Healthcare Disclaimer

⚠️ **Important**: This MCP server is designed to assist healthcare professionals and provide preliminary assessments. It is **NOT** a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified healthcare providers with any questions regarding medical conditions.

## License

MIT License - see LICENSE file for details.

## Authors
- Mathéo Vovard <MathVov.91@outlook.fr>
- Joao Gabriel <joao-gabriel.marques-dinis@efrei.net>
