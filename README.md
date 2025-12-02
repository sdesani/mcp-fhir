# FHIR MCP Server

A Model Context Protocol (MCP) server for interacting with FHIR APIs, specifically designed for Oracle Millennium Platform APIs. This server provides comprehensive tools for accessing various FHIR resources including Patient records, Clinical data, and Administrative information.

## Features

- **OAuth2 Authentication**: Secure API access using bearer token authentication
- **Comprehensive FHIR Resources**: Support for 10+ FHIR resource types
- **Patient Search**: Multiple search capabilities (name, identifier, birthdate, phone, email, address)
- **Clinical Data**: Access to allergies, conditions, procedures, observations, and immunizations
- **Medications & Diagnostics**: Retrieve medication requests and diagnostic reports
- **Appointments & Encounters**: Manage patient appointments and clinical encounters
- **Asynchronous Operations**: Efficient async/await implementation for better performance

## Supported FHIR Resources

1. **Patient** - Demographics and patient information
2. **AllergyIntolerance** - Patient allergy and intolerance records
3. **Condition** - Medical conditions and diagnoses
4. **Procedure** - Medical procedures performed
5. **Encounter** - Patient encounters and visits
6. **DiagnosticReport** - Diagnostic reports and results
7. **Observation** - Clinical observations (vital signs, lab results)
8. **Immunization** - Immunization records
9. **MedicationRequest** - Medication prescriptions and requests
10. **Appointment** - Scheduled appointments

## Installation

### Prerequisites

- Python 3.13 or higher
- `uv` package manager (recommended) or `pip`

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd fhir-mcp-server
```

2. Install dependencies using `uv`:
```bash
uv sync
```

Or using `pip`:
```bash
pip install -e .
```

3. Configure environment variables:

Create a `.env` file in the project directory and set your FHIR server details:
```bash
FHIR_BASE_URL=https://your-fhir-server.com/r4
OAUTH_BEARER_TOKEN=your_oauth2_bearer_token
```

The `.env` file should contain:
- `FHIR_CLIENT_ID`: Your OAuth2 client ID from the FHIR server provider
- `FHIR_CLIENT_SECRET`: Your OAuth2 client secret from the FHIR server provider
- `FHIR_BASE_URL`: The base URL of your FHIR R4 server endpoint
- `FHIR_TENANT_ID`: (Optional) Your tenant ID, defaults to Oracle Cerner sandbox
- `FHIR_SCOPE`: (Optional) OAuth2 scopes, defaults to all supported resources
- `FHIR_REQUEST_TIMEOUT`: (Optional) Request timeout in seconds, default is 60

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `FHIR_CLIENT_ID` | OAuth2 client ID for authentication | Yes | None |
| `FHIR_CLIENT_SECRET` | OAuth2 client secret for authentication | Yes | None |
| `FHIR_BASE_URL` | Base URL of the FHIR server | No | `https://fhir-ehr.cerner.com/r4` |
| `FHIR_TENANT_ID` | Tenant ID for your FHIR server instance | No | `ec2458f2-1e24-41c8-b71b-0e701af7583d` |
| `FHIR_TOKEN_ENDPOINT` | OAuth2 token endpoint URL | No | Auto-generated from tenant ID |
| `FHIR_SCOPE` | OAuth2 scopes (space-separated) | No | All supported resources |
| `FHIR_REQUEST_TIMEOUT` | Request timeout in seconds | No | `60.0` |

### OAuth2 Authentication

This server uses **OAuth 2.0 Client Credentials flow** for system-to-system authentication, following Oracle Cerner's SMART Backend Services specification.

#### Application Registration

Before using this server, you must register your application with Oracle Cerner to obtain client credentials:

1. **Create a CernerCare Account**
   - Sign up at [Oracle Cerner Code Console](https://code.cerner.com/)
   - Complete the account registration process

2. **Register Your Application**
   - Log in to the [Code Console](https://code.cerner.com/)
   - Navigate to "My Applications" and click "Register New Application"
   - Choose application type:
     - **System** - For backend services and automated systems
     - **Confidential** - For applications that can securely store credentials
   - Provide application details:
     - Application name
     - Description
     - Redirect URIs (not required for client credentials flow)
   - Complete the registration process

3. **Obtain Credentials**
   - After registration, you'll receive:
     - **Client ID** - Your application's unique identifier
     - **Client Secret** - Managed through Cerner Central system accounts
   - Store these credentials securely

4. **Configure FHIR Scopes**
   
   > **Note**: Scope format varies based on type of token requested. Below scopes format are for `SMART V2 Token`:
   
   Request the following system-level scopes for your application (SMART v1 format):
     - `system/Patient.rs` - Read access to patient resources
     - `system/Observation.rs` - Read access to observation resources
     - `system/Condition.rs` - Read access to condition resources
     - `system/Procedure.rs` - Read access to procedure resources
     - `system/Encounter.rs` - Read access to encounter resources
     - `system/DiagnosticReport.rs` - Read access to diagnostic reports
     - `system/AllergyIntolerance.rs` - Read access to allergy information
     - `system/Immunization.rs` - Read access to immunization records
     - `system/MedicationRequest.rs` - Read access to medication requests
     - `system/Appointment.rs` - Read access to appointments

#### Token Endpoint

The server automatically manages OAuth 2.0 tokens using Oracle Cerner's token endpoint:

```
https://authorization.cerner.com/tenants/{TENANT_ID}/hosts/fhir-ehr.cerner.com/protocols/oauth2/profiles/smart-v1/token
```

Default tenant ID: `ec2458f2-1e24-41c8-b71b-0e701af7583d` (Oracle Cerner Sandbox)

#### Automatic Token Management

The server automatically:
- Requests access tokens using client credentials on first API call
- Caches tokens until expiry
- Refreshes tokens automatically when needed (with 5-minute buffer before expiry)
- Handles token errors gracefully

#### Additional Resources

For more information about Oracle Cerner's authorization framework:
- [FHIR Authorization Framework](https://docs.oracle.com/en/industries/health/millennium-platform-apis/fhir-authorization-framework/#requesting-authorization-on-behalf-of-a-system)
- [Oracle Cerner Code Console](https://code.cerner.com/)
- [SMART Backend Services Specification](http://hl7.org/fhir/smart-app-launch/backend-services.html)

## Usage

### Running the Server

Run the MCP server using:

```bash
python fhir-mcp-server.py
```

Or if using `uv`:

```bash
uv run python fhir-mcp-server.py
```

### Using with Claude Desktop or Cursor

#### For Claude Desktop:

Add the following configuration to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "fhir": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "fastmcp",
        "run",
        "/absolute/path/to/fhir-mcp-server/fhir-mcp-server.py"
      ],
      "env": {
        "FHIR_CLIENT_ID": "your_client_id",
        "FHIR_CLIENT_SECRET": "your_client_secret",
        "FHIR_BASE_URL": "https://fhir-ehr.cerner.com/r4",
        "FHIR_TENANT_ID": "your_tenant_id"
      }
    }
  }
}
```

**Important**: Replace `/absolute/path/to/fhir-mcp-server/fhir-mcp-server.py` with the actual full path to the script!

#### For Cursor IDE:

Add the same configuration to Cursor's MCP settings. See **[QUICKSTART.md](QUICKSTART.md#option-b-cursor-ide)** for detailed Cursor-specific instructions including:
- Where to find Cursor's MCP configuration
- UI-based setup options
- Cursor-specific troubleshooting

## Available Tools

### Patient Tools

- `get_patient_by_id` - Retrieve a patient by ID
- `search_patients_by_name` - Search patients by given/family name
- `search_patients_by_identifier` - Search by identifier (MRN, SSN, etc.)
- `search_patients_by_birthdate` - Search by birth date
- `search_patients_by_phone` - Search by phone number
- `search_patients_by_email` - Search by email address
- `search_patients_by_address` - Search by address components

### Clinical Data Tools

- `get_allergy_by_id` / `get_patient_allergies` - Allergy information
- `get_condition_by_id` / `get_patient_conditions` - Medical conditions
- `get_procedure_by_id` / `get_patient_procedures` - Procedures
- `get_observation_by_id` / `get_patient_observations` - Observations
- `get_patient_vital_signs` - Vital signs specifically
- `get_patient_lab_results` - Laboratory results
- `get_immunization_by_id` / `get_patient_immunizations` - Immunizations

### Diagnostic & Medication Tools

- `get_diagnostic_report_by_id` / `get_patient_diagnostic_reports` - Diagnostic reports
- `get_medication_request_by_id` / `get_patient_medication_requests` - Medications

### Encounter & Appointment Tools

- `get_encounter_by_id` / `get_patient_encounters` - Patient encounters
- `get_appointment_by_id` / `get_patient_appointments` - Appointments
- `search_appointments_by_date` - Search appointments by date

### Utility Tools

- `get_fhir_capability_statement` - Get FHIR server capabilities

## Example Usage

### Example 1: Search for a Patient

```python
# Search for patients by name
result = await search_patients_by_name(
    given_name="John",
    family_name="Doe"
)
```

### Example 2: Get Patient's Medical History

```python
# Get patient's conditions
conditions = await get_patient_conditions(
    patient_id="12345",
    clinical_status="active"
)

# Get patient's allergies
allergies = await get_patient_allergies(
    patient_id="12345"
)

# Get patient's vital signs
vitals = await get_patient_vital_signs(
    patient_id="12345",
    date="2024-01-01"
)
```

### Example 3: Retrieve Appointments

```python
# Get upcoming appointments for a patient
appointments = await get_patient_appointments(
    patient_id="12345",
    status="booked",
    date="ge2024-01-01"  # Greater than or equal to date
)
```

## API Reference Documentation

This server implements tools based on the following Oracle Millennium Platform API documentation:

- [Patient API](https://docs.oracle.com/en/industries/health/millennium-platform-apis/mfrap/api-patient.html)
- [AllergyIntolerance API](https://docs.oracle.com/en/industries/health/millennium-platform-apis/mfrap/api-allergyintolerance.html)
- [Condition API](https://docs.oracle.com/en/industries/health/millennium-platform-apis/mfrap/api-condition.html)
- [Procedure API](https://docs.oracle.com/en/industries/health/millennium-platform-apis/mfrap/api-procedure.html)
- [Encounter API](https://docs.oracle.com/en/industries/health/millennium-platform-apis/mfrap/api-encounter.html)
- [DiagnosticReport API](https://docs.oracle.com/en/industries/health/millennium-platform-apis/mfrap/api-diagnosticreport.html)
- [Observation API](https://docs.oracle.com/en/industries/health/millennium-platform-apis/mfrap/api-observation.html)
- [Immunization API](https://docs.oracle.com/en/industries/health/millennium-platform-apis/mfrap/api-immunization.html)
- [MedicationRequest API](https://docs.oracle.com/en/industries/health/millennium-platform-apis/mfrap/api-medicationrequest.html)
- [Appointment API](https://docs.oracle.com/en/industries/health/millennium-platform-apis/mfrap/api-appointment.html)

## FHIR Standards

This server follows the [FHIR R4 specification](https://hl7.org/fhir/R4/) for resource structures and search parameters.

## Error Handling

The server will raise HTTP exceptions for:
- Authentication failures (401 Unauthorized)
- Missing resources (404 Not Found)
- Server errors (500 Internal Server Error)
- Invalid requests (400 Bad Request)

All exceptions include detailed error messages from the FHIR server response.

## Troubleshooting

### ModuleNotFoundError: No module named 'httpx' (or other dependencies)

**Problem**: Claude Desktop shows `ModuleNotFoundError` when trying to load the MCP server.

**Solution**: Make sure you've installed dependencies first:

```bash
cd /Users/sdesani/Work/fhir-mcp-server
uv sync
```

Your Claude Desktop config should use the `fastmcp run` pattern:

```json
{
  "command": "uv",
  "args": [
    "run",
    "--with",
    "fastmcp",
    "fastmcp",
    "run",
    "/absolute/path/to/fhir-mcp-server/fhir-mcp-server.py"
  ]
}
```

This uses `uv run --with fastmcp` to dynamically install FastMCP, then runs your script which will use the installed dependencies from your project's `.venv`.

### Other Common Issues

**Server not appearing in Claude Desktop**:
- Restart Claude Desktop after updating the config
- Check for JSON syntax errors in `claude_desktop_config.json`
- Verify the file path is absolute (starts with `/`)

**401 Unauthorized errors**:
- Verify your OAuth token is valid and not expired
- Check the token has the correct scopes/permissions

**Timeout errors**:
- Increase `FHIR_REQUEST_TIMEOUT` in your `.env` file or Claude Desktop config
- Default is 60 seconds, try 120 or higher for slow servers

## Security Considerations

- **Credential Management**: 
  - Never commit your `.env` file or credentials to version control
  - Store `FHIR_CLIENT_ID` and `FHIR_CLIENT_SECRET` securely
  - Use environment variables or secure credential management systems
  - Rotate credentials regularly according to your organization's security policies

- **OAuth 2.0 Security**:
  - The server uses OAuth 2.0 Client Credentials flow for secure system-to-system authentication
  - Tokens are automatically cached and refreshed
  - Follow the [Application Registration](#application-registration) steps to obtain valid credentials

- **HTTPS Only**: Always use HTTPS endpoints for production FHIR servers

- **Scope Management**: 
  - Request only the minimum required scopes for your application
  - Review and update scopes as your application requirements change
  - See [Application Registration](#application-registration) for available scopes

- **PHI Protection**: 
  - Be mindful that FHIR resources contain Protected Health Information (PHI)
  - Ensure compliance with healthcare data privacy regulations (HIPAA, GDPR, etc.)
  - Implement appropriate access controls and audit logging
  - Follow your organization's data handling policies

- **SMART Compliance**: 
  - This server follows the SMART Backend Services specification
  - Ensures secure healthcare application integration

## Development

### Project Structure

```
fhir-mcp-server/
├── fhir-mcp-server.py   # MCP server implementation
├── pyproject.toml       # Project dependencies and metadata
├── .env                 # Your local configuration (not committed)
├── .gitignore          # Git ignore rules
├── README.md           # This file
├── QUICKSTART.md       # Quick start guide
└── EXAMPLES.md         # Usage examples
```

### Adding New FHIR Resources

To add support for additional FHIR resources:

1. Add a new tool function decorated with `@mcp.tool()`
2. Use the `make_fhir_request()` helper function
3. Follow the existing pattern for parameters and return types
4. Update this README with the new tool information

### Testing

Test the server by running it and connecting through an MCP client like Cursor or using the MCP Inspector tool.

## License

[Add your license information here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues related to:
- **FHIR Server**: Contact your FHIR server administrator
- **Oracle Millennium Platform**: Refer to Oracle documentation
- **This MCP Server**: Open an issue in this repository

## Additional Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide with setup instructions for Claude Desktop and Cursor
- **[EXAMPLES.md](EXAMPLES.md)** - Comprehensive usage examples

## Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Implements [FHIR R4](https://hl7.org/fhir/R4/) standard
- Designed for [Oracle Millennium Platform APIs](https://docs.oracle.com/en/industries/health/millennium-platform-apis/)
