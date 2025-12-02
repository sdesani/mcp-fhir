# Quick Start Guide

Get your FHIR MCP Server up and running in 5 minutes!

## Step 1: Install Dependencies

```bash
# Make sure you're in the project directory
cd fhir-mcp-server

# Install using uv (recommended)
uv sync

# OR using pip
pip install -e .
```

## Step 2: Configure Environment

Create a `.env` file in the project directory:

```bash
# Create and edit .env file with your credentials
nano .env  # or use your preferred editor
```

Your `.env` file should look like this:

```bash
# Required: OAuth2 Client Credentials
FHIR_CLIENT_ID=your_client_id_here
FHIR_CLIENT_SECRET=your_client_secret_here

# Required: FHIR Server Configuration
FHIR_BASE_URL=https://fhir-ehr.cerner.com/r4
FHIR_TENANT_ID=your_tenant_id_here

# Optional: Advanced Configuration
FHIR_REQUEST_TIMEOUT=60.0
```

**Notes**: 
- `FHIR_CLIENT_ID` and `FHIR_CLIENT_SECRET` are **required** for authentication
- **Don't have credentials yet?** See [README.md - OAuth2 Authentication](README.md#oauth2-authentication) for detailed instructions on registering your SMART app with Oracle Cerner Code Console
- The server automatically manages OAuth2 tokens (requests, caches, and refreshes)
- `FHIR_REQUEST_TIMEOUT` is optional and defaults to 60 seconds if not specified
- `FHIR_SCOPE` can be customized to request specific resource permissions
  - **Note**: Use SMART v1 format (`.rs` suffix) for Oracle Cerner, or v2 format (`.read` suffix) for other servers - see [README.md](README.md#application-registration) for details

## Step 3: Test the Server

Run the server to make sure it starts correctly:

```bash
python fhir-mcp-server.py
```

You should see the MCP server start without errors.

## Step 4: Configure Your MCP Client

### Option A: Claude Desktop

#### Configuration Location
- **Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

#### Configuration

Add this to your Claude Desktop configuration:

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

**Important**: 
- Replace `/absolute/path/to/fhir-mcp-server/fhir-mcp-server.py` with the actual full path to the script
- This uses `uv run --with fastmcp fastmcp run` which dynamically installs FastMCP and runs your script
- Restart Claude Desktop after updating the configuration

#### Why This Configuration Works

This configuration:
- Uses `uv run --with fastmcp` to dynamically install and use FastMCP
- Runs `fastmcp run <script>` which launches your MCP server
- The script imports from the installed dependencies in your project's `.venv`
- Requires dependencies to be pre-installed with `uv sync`

### Option B: Cursor IDE

#### Configuration Location
Cursor's MCP configuration is typically stored at:
- **Mac/Linux**: `~/.cursor/mcp.json` or via Cursor Settings
- **Windows**: `%USERPROFILE%\.cursor\mcp.json`

Or access via:
1. Open Cursor
2. Go to **Cursor Settings** > **Features** > **MCP**
3. Or use Command Palette (`Cmd+Shift+P`) and search for "MCP Settings"

#### Configuration

Add this to your Cursor MCP configuration:

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

**Important**: Update the paths and credentials with your actual values.

#### Reload Cursor

After saving the configuration:
1. Restart Cursor completely (Quit and reopen)
2. Or reload the window: `Cmd+Shift+P` → "Developer: Reload Window"

### Option C: Using .env File (Recommended)

Instead of putting credentials in the MCP client config, you can use the `.env` file in the project:

1. Create your `.env` file (already covered in Step 2)

2. Simplified client config (Claude Desktop or Cursor):
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
      ]
    }
  }
}
```

The server will automatically load credentials from `.env`.

## Step 5: Test Your First Query

Once connected to your MCP client, try asking:

```
"Search for a patient named John Smith"
```

or

```
"Get the medical conditions for patient ID 12345"
```

## Quick Reference: Common Commands

### Patient Search
- "Search for patients with last name Smith"
- "Find patient by MRN 12345678"
- "Get patient by ID 12345"

### Clinical Data
- "Get active medical conditions for patient 12345"
- "Show allergies for patient 12345"
- "Get recent vital signs for patient 12345"

### Medications & Immunizations
- "Show active medications for patient 12345"
- "Get immunization history for patient 12345"

### Appointments
- "Get upcoming appointments for patient 12345"
- "Show all appointments for today"

## Available Tools

The FHIR MCP server provides 35+ tools:

### Patient Search
- `search_patients_by_name` - Search by first/last name
- `search_patients_by_identifier` - Search by MRN, SSN, etc.
- `search_patients_by_birthdate` - Search by birth date
- `search_patients_by_phone` - Search by phone number
- `search_patients_by_email` - Search by email
- `search_patients_by_address` - Search by address

### Clinical Data
- `get_patient_allergies` - Patient allergies
- `get_patient_conditions` - Medical conditions
- `get_patient_procedures` - Procedures performed
- `get_patient_observations` - Clinical observations
- `get_patient_vital_signs` - Vital signs
- `get_patient_lab_results` - Laboratory results
- `get_patient_immunizations` - Immunization records

### Medications & Reports
- `get_patient_medication_requests` - Active medications
- `get_patient_diagnostic_reports` - Diagnostic reports

### Appointments & Encounters
- `get_patient_appointments` - Patient appointments
- `get_patient_encounters` - Clinical encounters
- `search_appointments_by_date` - Search by date

## Troubleshooting

### "ModuleNotFoundError: No module named 'httpx'" in MCP Client

**Solution**: Make sure dependencies are installed first:
```bash
cd /path/to/fhir-mcp-server
uv sync
```

Then ensure your MCP client config uses the correct pattern:
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

This dynamically installs FastMCP and runs your script with its dependencies from `.venv`.

### "Import errors" when running locally

**Solution**: Install dependencies with `uv sync` or `pip install -e .`

### "FHIR_CLIENT_ID and FHIR_CLIENT_SECRET not set" error

**Solution**: Make sure your `.env` file exists and contains the client credentials, OR set them in your MCP client config env section

### "401 Unauthorized" errors

**Solution**: 
- Verify your client credentials are correct
- Check if your credentials have the required scopes/permissions
- Ensure the token endpoint is correct

### "Connection refused" or "Cannot connect to server"

**Solution**:
- Verify the `FHIR_BASE_URL` is correct
- Check your network connection
- Ensure the FHIR server is accessible from your machine

### "404 Not Found" for resources

**Solution**:
- Verify the patient ID or resource ID exists
- Check if you're using the correct ID format

### Server not showing up in Claude Desktop or Cursor

**Solution**:
- Restart your MCP client after config changes
- Check JSON syntax (no trailing commas)
- Verify all paths are absolute (start with `/`)
- Check that `.venv` directory exists in the project

### Permission errors

**Solution**:
- Ensure you have read/write access to the project directory
- Check that `uv` is installed: `uv --version`
- Verify your MCP client has permission to execute `uv`

### Testing Configuration Manually

Test the command manually before adding to your MCP client:

```bash
cd /path/to/fhir-mcp-server
uv run --with fastmcp fastmcp run fhir-mcp-server.py
```

You should see the FastMCP startup banner without any import errors.

## Environment Variables Reference

You can set these in the `env` section of your MCP client config or in the `.env` file:

```json
"env": {
  "FHIR_CLIENT_ID": "your_client_id",
  "FHIR_CLIENT_SECRET": "your_client_secret",
  "FHIR_BASE_URL": "https://fhir-ehr.cerner.com/r4",
  "FHIR_TENANT_ID": "your_tenant_id",
  "FHIR_SCOPE": "system/Patient.rs system/Observation.rs system/Appointment.rs",
  "FHIR_REQUEST_TIMEOUT": "120"
}
```

- `FHIR_CLIENT_ID`: OAuth2 client ID (required)
- `FHIR_CLIENT_SECRET`: OAuth2 client secret (required)
- `FHIR_BASE_URL`: Base URL of FHIR server (optional, has default)
- `FHIR_TENANT_ID`: Tenant ID for multi-tenant servers (optional)
- `FHIR_SCOPE`: OAuth2 scopes in SMART v1 format with `.rs` suffix (optional, has default)
- `FHIR_REQUEST_TIMEOUT`: Timeout in seconds (optional, default: 60)

## Getting Help

1. Check the full [README.md](README.md) for detailed documentation
2. Review [EXAMPLES.md](EXAMPLES.md) for usage patterns
3. Verify your FHIR server's API documentation
4. Check the [FHIR R4 specification](https://hl7.org/fhir/R4/)

## Next Steps

- Review available tools above
- Explore example queries in [EXAMPLES.md](EXAMPLES.md)
- Check your FHIR server's capability statement: `get_fhir_capability_statement()`
- Read about [FHIR search parameters](https://hl7.org/fhir/R4/search.html)

## Security Reminder

⚠️ **Important**: 
- Never commit your `.env` file to version control
- Keep your OAuth credentials secure
- Use HTTPS endpoints only for production
- Be mindful of PHI (Protected Health Information) handling requirements

Happy querying! 🚀
