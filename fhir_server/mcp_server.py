"""
FHIR MCP Server - Model Context Protocol Server for FHIR API Interactions
Supports Oracle Millennium Platform APIs for various FHIR resources.
"""

from fastmcp import FastMCP
import fhir_server.server as fhir_server


# Initialize MCP server
mcp = FastMCP("FHIR MCP Server")

# ============================================================================
# PATIENT RESOURCE TOOLS
# ============================================================================
mcp.tool(fhir_server.get_patient_by_id)
mcp.tool(fhir_server.search_patients_by_name)
mcp.tool(fhir_server.search_patients_by_identifier)
mcp.tool(fhir_server.search_patients_by_birthdate)
mcp.tool(fhir_server.search_patients_by_phone)
mcp.tool(fhir_server.search_patients_by_email)
mcp.tool(fhir_server.search_patients_by_address)

# ============================================================================
# ALLERGY INTOLERANCE RESOURCE TOOLS
# ============================================================================
mcp.tool(fhir_server.get_allergy_by_id)
mcp.tool(fhir_server.get_patient_allergies)

# ============================================================================
# CONDITION RESOURCE TOOLS
# ============================================================================
mcp.tool(fhir_server.get_condition_by_id)
mcp.tool(fhir_server.get_patient_conditions)

# ============================================================================
# PROCEDURE RESOURCE TOOLS
# ============================================================================
mcp.tool(fhir_server.get_procedure_by_id)
mcp.tool(fhir_server.get_patient_procedures)

# ============================================================================
# ENCOUNTER RESOURCE TOOLS
# ============================================================================
mcp.tool(fhir_server.get_encounter_by_id)
mcp.tool(fhir_server.get_patient_encounters)

# ============================================================================
# DIAGNOSTIC REPORT RESOURCE TOOLS
# ============================================================================
mcp.tool(fhir_server.get_diagnostic_report_by_id)
mcp.tool(fhir_server.get_patient_diagnostic_reports)

# ============================================================================
# OBSERVATION RESOURCE TOOLS
# ============================================================================
mcp.tool(fhir_server.get_observation_by_id)
mcp.tool(fhir_server.get_patient_observations)
mcp.tool(fhir_server.get_patient_vital_signs)
mcp.tool(fhir_server.get_patient_lab_results)

# ============================================================================
# IMMUNIZATION RESOURCE TOOLS
# ============================================================================
mcp.tool(fhir_server.get_immunization_by_id)
mcp.tool(fhir_server.get_patient_immunizations)

# ============================================================================
# MEDICATION REQUEST RESOURCE TOOLS
# ============================================================================
mcp.tool(fhir_server.get_medication_request_by_id)
mcp.tool(fhir_server.get_patient_medication_requests)

# ============================================================================
# APPOINTMENT RESOURCE TOOLS
# ============================================================================
mcp.tool(fhir_server.get_appointment_by_id)
mcp.tool(fhir_server.get_patient_appointments)
mcp.tool(fhir_server.search_appointments_by_date)

# ============================================================================
# UTILITY TOOLS
# ============================================================================
mcp.tool(fhir_server.get_fhir_capability_statement)
