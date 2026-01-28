# Carestral MCP Server - Usage Examples

## Example 1: Assessing Common Symptoms

When a patient presents with fever and cough:

```json
{
  "tool": "assess_symptoms",
  "arguments": {
    "symptoms": ["fever", "cough"],
    "duration": "3 days",
    "severity": "moderate"
  }
}
```

Expected output:
- Severity assessment
- Red flag warnings
- Recommended specialties (General Practice, Pulmonology)
- Next steps

## Example 2: Urgent Care Scenario

Patient with chest pain:

```json
{
  "tool": "assess_symptoms",
  "arguments": {
    "symptoms": ["chest_pain"],
    "duration": "1 hour",
    "severity": "severe"
  }
}
```

Expected output:
- High severity warning
- Urgent care flag
- Cardiology or Emergency Medicine referral
- Immediate action recommendations

## Example 3: Finding a Specialist

```json
{
  "tool": "find_specialist",
  "arguments": {
    "condition": "abdominal_pain",
    "urgency": "routine"
  }
}
```

Expected output:
- Gastroenterology recommendation
- Wait time information
- Specialty description

## Example 4: Emergency Routing

```json
{
  "tool": "find_specialist",
  "arguments": {
    "condition": "severe_bleeding",
    "urgency": "emergency"
  }
}
```

Expected output:
- Immediate emergency department directive
- Emergency Medicine specialty

## Example 5: Creating a Medical Referral

```json
{
  "tool": "create_referral",
  "arguments": {
    "patient_id": "P12345",
    "specialty": "cardiology",
    "symptoms": "Intermittent chest pain, palpitations, shortness of breath on exertion",
    "priority": "urgent"
  }
}
```

Expected output:
- Unique referral ID
- Priority level
- Specialty information
- Next steps for patient

## Prompt Template: Patient Triage

Use the `triage_patient` prompt for interactive assessment:

```json
{
  "prompt": "triage_patient",
  "arguments": {
    "symptoms": "severe headache with visual changes",
    "duration": "2 hours"
  }
}
```

The AI will:
1. Use assess_symptoms tool
2. Check for red flags
3. Determine urgency
4. Recommend specialist if needed
5. Provide compassionate guidance

## Prompt Template: Referral Letter

Generate a professional referral:

```json
{
  "prompt": "referral_letter",
  "arguments": {
    "patient_name": "Jane Doe",
    "condition": "persistent chest pain",
    "specialist": "cardiology"
  }
}
```

## Resource Access

### Viewing Symptom Database

```
Resource: carestral://symptoms/database
```

Returns JSON with all symptoms in the database including severity, urgency flags, specialties, and red flags.

### Viewing Specialty Information

```
Resource: carestral://specialties/list
```

Returns JSON with all medical specialties, descriptions, and typical wait times.

## Integration with Claude Desktop

1. Open Claude Desktop configuration file
2. Add Carestral MCP server:

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

3. Restart Claude Desktop
4. Start using Carestral tools in your conversations!

## Common Workflows

### Workflow 1: New Patient Assessment

1. Patient describes symptoms → Use `assess_symptoms`
2. Review assessment output → Check red flags
3. If specialist needed → Use `find_specialist`
4. Create formal referral → Use `create_referral`

### Workflow 2: Emergency Triage

1. Quick symptom check → Use `assess_symptoms`
2. If urgent flag raised → Use `find_specialist` with urgency="emergency"
3. Direct to emergency department

### Workflow 3: Routine Care Coordination

1. Known condition → Use `find_specialist` directly
2. Create referral → Use `create_referral`
3. Patient receives appointment information

## Tips for Best Results

- **Be specific**: Include as many relevant symptoms as possible
- **Include duration**: Time context helps with severity assessment
- **Note red flags**: The system will identify concerning symptoms
- **Use appropriate urgency**: Choose between routine, urgent, or emergency
- **Complete referrals**: Provide detailed symptom summaries for referrals
