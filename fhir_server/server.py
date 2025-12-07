import os
import re
import time
import base64
from typing import Optional, Dict, Any
import httpx

# Configuration
FHIR_BASE_URL = os.getenv("FHIR_BASE_URL", "https://fhir-ehr.cerner.com/r4")
FHIR_TENANT_ID = os.getenv("FHIR_TENANT_ID", "ec2458f2-1e24-41c8-b71b-0e701af7583d")
FHIR_CLIENT_ID = os.getenv("FHIR_CLIENT_ID", "")
FHIR_CLIENT_SECRET = os.getenv("FHIR_CLIENT_SECRET", "")
FHIR_TOKEN_ENDPOINT = os.getenv(
    "FHIR_TOKEN_ENDPOINT",
    f"https://authorization.cerner.com/tenants/{FHIR_TENANT_ID}/hosts/fhir-ehr.cerner.com/protocols/oauth2/profiles/smart-v1/token",
)
FHIR_SCOPE = os.getenv("FHIR_SCOPE", "system/Patient.rs system/Appointment.rs")
REQUEST_TIMEOUT = float(os.getenv("FHIR_REQUEST_TIMEOUT", "60.0"))

# Token management
ACCESS_TOKEN = None
TOKEN_EXPIRES_AT = 0

# Validation
if not FHIR_CLIENT_ID or not FHIR_CLIENT_SECRET:
    raise ValueError(
        "FHIR_CLIENT_ID and FHIR_CLIENT_SECRET environment variables must be set"
    )


async def get_access_token() -> str:
    """
    Get a valid access token, refreshing if necessary.
    Uses OAuth 2.0 client credentials flow for system-to-system authentication.

    Returns:
        Valid access token string

    Raises:
        ValueError: If client credentials are not configured
        httpx.HTTPError: If token request fails
    """
    global ACCESS_TOKEN, TOKEN_EXPIRES_AT

    if not FHIR_CLIENT_ID or not FHIR_CLIENT_SECRET:
        raise ValueError(
            "FHIR_CLIENT_ID and FHIR_CLIENT_SECRET must be set in environment variables"
        )

    # Check if current token is still valid (with 5-minute buffer)
    if ACCESS_TOKEN and time.time() < (TOKEN_EXPIRES_AT - 300):
        return ACCESS_TOKEN

    # Request new token using client credentials flow
    token_data = {"grant_type": "client_credentials", "scope": FHIR_SCOPE}

    # Create Basic Auth header with client credentials
    credentials = f"{FHIR_CLIENT_ID}:{FHIR_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "Authorization": f"Basic {encoded_credentials}",
    }

    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.post(
                FHIR_TOKEN_ENDPOINT, data=token_data, headers=headers
            )
            response.raise_for_status()

            token_response = response.json()
            ACCESS_TOKEN = token_response["access_token"]
            expires_in = token_response.get("expires_in", 3600)  # Default to 1 hour
            TOKEN_EXPIRES_AT = time.time() + expires_in

            return ACCESS_TOKEN

    except httpx.HTTPError as e:
        raise httpx.HTTPError(f"Failed to obtain access token: {str(e)}")


async def get_headers() -> Dict[str, str]:
    """Get HTTP headers with OAuth2 bearer token (dynamically generated)"""
    access_token = await get_access_token()

    return {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/fhir+json",
        "Content-Type": "application/fhir+json",
    }


async def make_fhir_request(
    resource_type: str,
    resource_id: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Make a FHIR API request

    Args:
        resource_type: FHIR resource type (e.g., 'Patient', 'Observation')
        resource_id: Optional resource ID for specific resource retrieval
        params: Optional query parameters for search

    Returns:
        Dictionary containing the FHIR response
    """
    url = f"{FHIR_BASE_URL}/{FHIR_TENANT_ID}/{resource_type}"
    if resource_id:
        url = f"{url}/{resource_id}"

    headers = await get_headers()

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.get(url, headers=headers, params=params or {})
        response.raise_for_status()
        return response.json()


# ============================================================================
# PATIENT RESOURCE TOOLS
# ============================================================================


async def get_patient_by_id(patient_id: str) -> Dict[str, Any]:
    """
    Retrieve a specific patient by their FHIR patient ID.

    Args:
        patient_id: The FHIR patient ID to retrieve

    Returns:
        Dictionary containing the patient information
    """
    return await make_fhir_request("Patient", patient_id)


async def search_patients_by_name(
    given_name: Optional[str] = None, family_name: Optional[str] = None
) -> dict[str, Any]:
    """
    Search for patients by name using FHIR search parameters.

    Args:
        given_name: Patient's given (first) name
        family_name: Patient's family (last) name

    Returns:
        Dictionary containing the search results"""
    params = {}
    if given_name:
        params["given"] = given_name
    if family_name:
        params["family"] = family_name

    return await make_fhir_request("Patient", params=params)


async def search_patients_by_identifier(
    identifier_type: str, identifier_value: str
) -> Dict[str, Any]:
    """
    Search for patients by identifier (e.g., MRN, SSN).

    Args:
        identifier_type: Type of identifier (e.g., "MR", "SS")
        identifier_value: The identifier value to search for

    Returns:
        Dictionary containing the search results"""
    params = {"identifier": f"{identifier_type}|{identifier_value}"}
    return await make_fhir_request("Patient", params=params)


async def search_patients_by_birthdate(birthdate: str) -> Dict[str, Any]:
    """
    Search for patients by birth date.

    Args:
        birthdate: Patient's birth date in YYYY-MM-DD format

    Returns:
        Dictionary containing the search results"""
    params = {"birthdate": birthdate}
    return await make_fhir_request("Patient", params=params)


async def search_patients_by_phone(phone_number: str) -> Dict[str, Any]:
    """
    Search for patients by phone number.

    Args:
        phone_number: Patient's phone number

    Returns:
        Dictionary containing the search results"""
    params = {"telecom": phone_number}
    return await make_fhir_request("Patient", params=params)


async def search_patients_by_email(email: str) -> Dict[str, Any]:
    """
    Search for patients by email address.

    Args:
        email: Patient's email address

    Returns:
        Dictionary containing the search results"""
    params = {"email": email}
    return await make_fhir_request("Patient", params=params)


async def search_patients_by_address(
    postal_code: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Search for patients by address components.

    Args:
        postal_code: Patient's postal/ZIP code
        city: Patient's city
        state: Patient's state

    Returns:
        Dictionary containing the search results"""
    params = {}
    if postal_code:
        params["address-postalcode"] = postal_code
    if city:
        params["address-city"] = city
    if state:
        params["address-state"] = state

    return await make_fhir_request("Patient", params=params)


# ============================================================================
# ALLERGY INTOLERANCE RESOURCE TOOLS
# ============================================================================


async def get_allergy_by_id(allergy_id: str) -> Dict[str, Any]:
    """
    Retrieve a specific allergy intolerance by ID.

    Args:
        allergy_id: The FHIR AllergyIntolerance ID

    Returns:
        Dictionary containing the allergy intolerance information
    """
    return await make_fhir_request("AllergyIntolerance", allergy_id)


async def get_patient_allergies(
    patient_id: str, clinical_status: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve allergies for a specific patient.

    Args:
        patient_id: The FHIR patient ID
        clinical_status: Optional filter by clinical status (active, inactive, resolved)

    Returns:
        Dictionary containing the patient's allergies"""
    params = {"patient": patient_id}
    if clinical_status:
        params["clinical-status"] = clinical_status

    return await make_fhir_request("AllergyIntolerance", params=params)


# ============================================================================
# CONDITION RESOURCE TOOLS
# ============================================================================


async def get_condition_by_id(condition_id: str) -> Dict[str, Any]:
    """
    Retrieve a specific condition by ID.

    Args:
        condition_id: The FHIR Condition ID

    Returns:
        Dictionary containing the condition information
    """
    return await make_fhir_request("Condition", condition_id)


async def get_patient_conditions(
    patient_id: str,
    clinical_status: Optional[str] = None,
    category: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Retrieve conditions for a specific patient.

    Args:
        patient_id: The FHIR patient ID
        clinical_status: Optional filter by clinical status (active, inactive, resolved)
        category: Optional filter by category (problem-list-item, encounter-diagnosis)

    Returns:
        Dictionary containing the patient's conditions"""
    params = {"patient": patient_id}
    if clinical_status:
        params["clinical-status"] = clinical_status
    if category:
        params["category"] = category

    return await make_fhir_request("Condition", params=params)


# ============================================================================
# PROCEDURE RESOURCE TOOLS
# ============================================================================


async def get_procedure_by_id(procedure_id: str) -> Dict[str, Any]:
    """
    Retrieve a specific procedure by ID.

    Args:
        procedure_id: The FHIR Procedure ID

    Returns:
        Dictionary containing the procedure information
    """
    return await make_fhir_request("Procedure", procedure_id)


async def get_patient_procedures(
    patient_id: str, date: Optional[str] = None, status: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve procedures for a specific patient.

    Args:
        patient_id: The FHIR patient ID
        date: Optional filter by date (YYYY-MM-DD format or date range)
        status: Optional filter by status (preparation, in-progress, completed)

    Returns:
        Dictionary containing the patient's procedures"""
    params = {"patient": patient_id}
    if date:
        params["date"] = date
    if status:
        params["status"] = status

    return await make_fhir_request("Procedure", params=params)


# ============================================================================
# ENCOUNTER RESOURCE TOOLS
# ============================================================================


async def get_encounter_by_id(encounter_id: str) -> Dict[str, Any]:
    """
    Retrieve a specific encounter by ID.

    Args:
        encounter_id: The FHIR Encounter ID

    Returns:
        Dictionary containing the encounter information
    """
    return await make_fhir_request("Encounter", encounter_id)


async def get_patient_encounters(
    patient_id: str,
    date: Optional[str] = None,
    status: Optional[str] = None,
    encounter_class: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Retrieve encounters for a specific patient.

    Args:
        patient_id: The FHIR patient ID
        date: Optional filter by date (YYYY-MM-DD format or date range)
        status: Optional filter by status (planned, arrived, in-progress, finished)
        encounter_class: Optional filter by class (ambulatory, emergency, inpatient)

    Returns:
        Dictionary containing the patient's encounters"""
    params = {"patient": patient_id}
    if date:
        params["date"] = date
    if status:
        params["status"] = status
    if encounter_class:
        params["class"] = encounter_class

    return await make_fhir_request("Encounter", params=params)


# ============================================================================
# DIAGNOSTIC REPORT RESOURCE TOOLS
# ============================================================================


async def get_diagnostic_report_by_id(report_id: str) -> Dict[str, Any]:
    """
    Retrieve a specific diagnostic report by ID.

    Args:
        report_id: The FHIR DiagnosticReport ID

    Returns:
        Dictionary containing the diagnostic report information
    """
    return await make_fhir_request("DiagnosticReport", report_id)


async def get_patient_diagnostic_reports(
    patient_id: str,
    category: Optional[str] = None,
    date: Optional[str] = None,
    status: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Retrieve diagnostic reports for a specific patient.

    Args:
        patient_id: The FHIR patient ID
        category: Optional filter by category (LAB, RAD, etc.)
        date: Optional filter by date (YYYY-MM-DD format or date range)
        status: Optional filter by status (registered, partial, final, corrected)

    Returns:
        Dictionary containing the patient's diagnostic reports"""
    params = {"patient": patient_id}
    if category:
        params["category"] = category
    if date:
        params["date"] = date
    if status:
        params["status"] = status

    return await make_fhir_request("DiagnosticReport", params=params)


# ============================================================================
# OBSERVATION RESOURCE TOOLS
# ============================================================================


async def get_observation_by_id(observation_id: str) -> Dict[str, Any]:
    """
    Retrieve a specific observation by ID.

    Args:
        observation_id: The FHIR Observation ID

    Returns:
        Dictionary containing the observation information
    """
    return await make_fhir_request("Observation", observation_id)


async def get_patient_observations(
    patient_id: str,
    category: Optional[str] = None,
    code: Optional[str] = None,
    date: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Retrieve observations for a specific patient.

    Args:
        patient_id: The FHIR patient ID
        category: Optional filter by category (vital-signs, laboratory, etc.)
        code: Optional filter by observation code (LOINC code)
        date: Optional filter by date (YYYY-MM-DD format or date range)

    Returns:
        Dictionary containing the patient's observations"""
    params = {"patient": patient_id}
    if category:
        params["category"] = category
    if code:
        params["code"] = code
    if date:
        params["date"] = date

    return await make_fhir_request("Observation", params=params)


async def get_patient_vital_signs(
    patient_id: str, date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve vital signs observations for a specific patient.

    Args:
        patient_id: The FHIR patient ID
        date: Optional filter by date (YYYY-MM-DD format or date range)

    Returns:
        Dictionary containing the patient's vital signs"""
    params = {"patient": patient_id, "category": "vital-signs"}
    if date:
        params["date"] = date

    return await make_fhir_request("Observation", params=params)


async def get_patient_lab_results(
    patient_id: str, date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve laboratory observations for a specific patient.

    Args:
        patient_id: The FHIR patient ID
        date: Optional filter by date (YYYY-MM-DD format or date range)

    Returns:
        Dictionary containing the patient's lab results"""
    params = {"patient": patient_id, "category": "laboratory"}
    if date:
        params["date"] = date

    return await make_fhir_request("Observation", params=params)


# ============================================================================
# IMMUNIZATION RESOURCE TOOLS
# ============================================================================


async def get_immunization_by_id(immunization_id: str) -> Dict[str, Any]:
    """
    Retrieve a specific immunization by ID.

    Args:
        immunization_id: The FHIR Immunization ID

    Returns:
        Dictionary containing the immunization information
    """
    return await make_fhir_request("Immunization", immunization_id)


async def get_patient_immunizations(
    patient_id: str, date: Optional[str] = None, status: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve immunizations for a specific patient.

    Args:
        patient_id: The FHIR patient ID
        date: Optional filter by date (YYYY-MM-DD format or date range)
        status: Optional filter by status (completed, not-done)

    Returns:
        Dictionary containing the patient's immunizations"""
    params = {"patient": patient_id}
    if date:
        params["date"] = date
    if status:
        params["status"] = status

    return await make_fhir_request("Immunization", params=params)


# ============================================================================
# MEDICATION REQUEST RESOURCE TOOLS
# ============================================================================


async def get_medication_request_by_id(medication_request_id: str) -> Dict[str, Any]:
    """
    Retrieve a specific medication request by ID.

    Args:
        medication_request_id: The FHIR MedicationRequest ID

    Returns:
        Dictionary containing the medication request information
    """
    return await make_fhir_request("MedicationRequest", medication_request_id)


async def get_patient_medication_requests(
    patient_id: str, status: Optional[str] = None, intent: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve medication requests for a specific patient.

    Args:
        patient_id: The FHIR patient ID
        status: Optional filter by status (active, completed, cancelled)
        intent: Optional filter by intent (order, plan, proposal)

    Returns:
        Dictionary containing the patient's medication requests"""
    params = {"patient": patient_id}
    if status:
        params["status"] = status
    if intent:
        params["intent"] = intent

    return await make_fhir_request("MedicationRequest", params=params)


# ============================================================================
# APPOINTMENT RESOURCE TOOLS
# ============================================================================


def format_appointment_date(date_str: str) -> str:
    """
    Format date string for Appointment API calls.

    If only a date (YYYY-MM-DD) is provided (with optional prefix like ge, le, gt, lt),
    automatically adds time component in ISO 8601 format (T00:00:00.000Z).

    Examples:
        - "2024-01-15" -> "2024-01-15T00:00:00.000Z"
        - "ge2024-01-15" -> "ge2024-01-15T00:00:00.000Z"
        - "ge2024-01-15T10:30:00.000Z" -> "ge2024-01-15T10:30:00.000Z" (unchanged)

    Args:
        date_str: Date string with optional FHIR prefix (ge, le, gt, lt, eq, ne, sa, eb, ap)

    Returns:
        Formatted date string with time component
    """
    if not date_str:
        return date_str

    # FHIR date comparison prefixes
    prefix_pattern = r"^(ge|le|gt|lt|eq|ne|sa|eb|ap)?"
    match = re.match(prefix_pattern, date_str)
    prefix = match.group(1) if match and match.group(1) else ""

    # Remove prefix to check the date portion
    date_part = date_str[len(prefix) :] if prefix else date_str

    # Check if time component is already present (contains 'T')
    if "T" in date_part:
        return date_str  # Already has time, return as-is

    # Check if it's a valid date format (YYYY-MM-DD)
    date_pattern = r"^\d{4}-\d{2}-\d{2}$"
    if re.match(date_pattern, date_part):
        # Add time component at midnight UTC
        return f"{prefix}{date_part}T00:00:00.000Z"

    # Return as-is if format doesn't match expected patterns
    return date_str


async def get_appointment_by_id(appointment_id: str) -> Dict[str, Any]:
    """
    Retrieve a specific appointment by ID.

    Args:
        appointment_id: The FHIR Appointment ID

    Returns:
        Dictionary containing the appointment information
    """
    return await make_fhir_request("Appointment", appointment_id)


async def get_patient_appointments(
    patient_id: str, date: Optional[str] = None, status: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve appointments for a specific patient.

    Args:
        patient_id: The FHIR patient ID
        date: Optional filter by date (YYYY-MM-DD format, automatically formatted with time component)
        status: Optional filter by status (proposed, pending, booked, arrived, fulfilled, cancelled)

    Returns:
        Dictionary containing the patient's appointments
    """
    params = {"patient": patient_id}
    if date:
        params["date"] = format_appointment_date(date)
    if status:
        params["status"] = status

    return await make_fhir_request("Appointment", params=params)


async def search_appointments_by_date(
    date: str, status: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for appointments by date.

    Args:
        date: Appointment date (YYYY-MM-DD format, automatically formatted with time component)
        status: Optional filter by status (proposed, pending, booked, arrived, fulfilled, cancelled)

    Returns:
        Dictionary containing the appointments
    """
    params = {"date": format_appointment_date(date)}
    if status:
        params["status"] = status

    return await make_fhir_request("Appointment", params=params)


# ============================================================================
# UTILITY TOOLS
# ============================================================================
async def get_fhir_capability_statement() -> dict[str, Any]:
    """
    Retrieve the FHIR server's capability statement (metadata).
    This provides information about the server's capabilities and supported resources.

    Returns:
        Dictionary containing the FHIR server capabilities
    """
    url = f"{FHIR_BASE_URL}/{FHIR_TENANT_ID}/metadata"
    headers = await get_headers()

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
