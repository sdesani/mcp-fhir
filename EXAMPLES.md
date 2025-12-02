# FHIR MCP Server - Usage Examples

This document provides practical examples of using the FHIR MCP Server tools to interact with FHIR resources.

## Table of Contents

- [Patient Search Examples](#patient-search-examples)
- [Clinical Data Examples](#clinical-data-examples)
- [Observations and Vital Signs](#observations-and-vital-signs)
- [Medications and Allergies](#medications-and-allergies)
- [Appointments and Encounters](#appointments-and-encounters)
- [Advanced Search Patterns](#advanced-search-patterns)

## Patient Search Examples

### Search by Name

```python
# Search for a patient by full name
result = await search_patients_by_name(
    given_name="John",
    family_name="Smith"
)

# Search by last name only
result = await search_patients_by_name(
    family_name="Smith"
)
```

### Search by Medical Record Number (MRN)

```python
# Search using MRN identifier
result = await search_patients_by_identifier(
    identifier_type="MR",
    identifier_value="12345678"
)
```

### Search by Demographics

```python
# Search by birth date
result = await search_patients_by_birthdate(
    birthdate="1990-05-15"
)

# Search by phone number
result = await search_patients_by_phone(
    phone_number="555-123-4567"
)

# Search by email
result = await search_patients_by_email(
    email="john.smith@example.com"
)

# Search by address
result = await search_patients_by_address(
    postal_code="12345",
    city="Springfield",
    state="IL"
)
```

### Get Specific Patient

```python
# Retrieve a patient by their FHIR ID
patient = await get_patient_by_id(patient_id="Patient/12345")
```

## Clinical Data Examples

### Patient Conditions

```python
# Get all active conditions for a patient
conditions = await get_patient_conditions(
    patient_id="12345",
    clinical_status="active"
)

# Get problem list items specifically
conditions = await get_patient_conditions(
    patient_id="12345",
    category="problem-list-item"
)

# Get encounter diagnoses
diagnoses = await get_patient_conditions(
    patient_id="12345",
    category="encounter-diagnosis"
)

# Get a specific condition by ID
condition = await get_condition_by_id(condition_id="Condition/67890")
```

### Patient Procedures

```python
# Get all procedures for a patient
procedures = await get_patient_procedures(
    patient_id="12345"
)

# Get procedures within a date range
procedures = await get_patient_procedures(
    patient_id="12345",
    date="ge2024-01-01",  # Greater than or equal to Jan 1, 2024
)

# Get completed procedures only
procedures = await get_patient_procedures(
    patient_id="12345",
    status="completed"
)

# Get a specific procedure
procedure = await get_procedure_by_id(procedure_id="Procedure/98765")
```

## Observations and Vital Signs

### Vital Signs

```python
# Get all vital signs for a patient
vitals = await get_patient_vital_signs(
    patient_id="12345"
)

# Get recent vital signs (last 30 days)
vitals = await get_patient_vital_signs(
    patient_id="12345",
    date="ge2024-10-20"
)
```

### Laboratory Results

```python
# Get all lab results for a patient
labs = await get_patient_lab_results(
    patient_id="12345"
)

# Get recent lab results
labs = await get_patient_lab_results(
    patient_id="12345",
    date="ge2024-01-01"
)
```

### General Observations

```python
# Get all observations for a patient
observations = await get_patient_observations(
    patient_id="12345"
)

# Get observations by category
observations = await get_patient_observations(
    patient_id="12345",
    category="vital-signs"
)

# Get observations by specific code (e.g., Blood Pressure)
observations = await get_patient_observations(
    patient_id="12345",
    code="85354-9",  # LOINC code for Blood Pressure
)

# Get observation by ID
observation = await get_observation_by_id(observation_id="Observation/11111")
```

## Medications and Allergies

### Allergies

```python
# Get all allergies for a patient
allergies = await get_patient_allergies(
    patient_id="12345"
)

# Get only active allergies
allergies = await get_patient_allergies(
    patient_id="12345",
    clinical_status="active"
)

# Get a specific allergy
allergy = await get_allergy_by_id(allergy_id="AllergyIntolerance/22222")
```

### Medication Requests

```python
# Get all medication requests for a patient
medications = await get_patient_medication_requests(
    patient_id="12345"
)

# Get active medications only
medications = await get_patient_medication_requests(
    patient_id="12345",
    status="active"
)

# Get medication orders specifically
medications = await get_patient_medication_requests(
    patient_id="12345",
    intent="order"
)

# Get a specific medication request
medication = await get_medication_request_by_id(
    medication_request_id="MedicationRequest/33333"
)
```

### Immunizations

```python
# Get all immunizations for a patient
immunizations = await get_patient_immunizations(
    patient_id="12345"
)

# Get immunizations from a specific date range
immunizations = await get_patient_immunizations(
    patient_id="12345",
    date="ge2020-01-01"
)

# Get completed immunizations only
immunizations = await get_patient_immunizations(
    patient_id="12345",
    status="completed"
)

# Get specific immunization
immunization = await get_immunization_by_id(
    immunization_id="Immunization/44444"
)
```

## Appointments and Encounters

### Appointments

```python
# Get all appointments for a patient
appointments = await get_patient_appointments(
    patient_id="12345"
)

# Get upcoming appointments
appointments = await get_patient_appointments(
    patient_id="12345",
    date="ge2024-11-19",  # From today onwards
    status="booked"
)

# Get appointments by status
appointments = await get_patient_appointments(
    patient_id="12345",
    status="fulfilled",  # or "cancelled", "pending", "proposed"
)

# Search appointments by date (across all patients)
appointments = await search_appointments_by_date(
    date="2024-11-20",
    status="booked"
)

# Get specific appointment
appointment = await get_appointment_by_id(
    appointment_id="Appointment/55555"
)
```

### Encounters

```python
# Get all encounters for a patient
encounters = await get_patient_encounters(
    patient_id="12345"
)

# Get encounters by date range
encounters = await get_patient_encounters(
    patient_id="12345",
    date="ge2024-01-01"
)

# Get encounters by status
encounters = await get_patient_encounters(
    patient_id="12345",
    status="finished"
)

# Get encounters by class (type)
encounters = await get_patient_encounters(
    patient_id="12345",
    encounter_class="ambulatory",  # or "emergency", "inpatient"
)

# Get specific encounter
encounter = await get_encounter_by_id(encounter_id="Encounter/66666")
```

### Diagnostic Reports

```python
# Get all diagnostic reports for a patient
reports = await get_patient_diagnostic_reports(
    patient_id="12345"
)

# Get lab reports only
lab_reports = await get_patient_diagnostic_reports(
    patient_id="12345",
    category="LAB"
)

# Get radiology reports
rad_reports = await get_patient_diagnostic_reports(
    patient_id="12345",
    category="RAD"
)

# Get final reports only
reports = await get_patient_diagnostic_reports(
    patient_id="12345",
    status="final"
)

# Get reports by date
reports = await get_patient_diagnostic_reports(
    patient_id="12345",
    date="ge2024-01-01"
)

# Get specific diagnostic report
report = await get_diagnostic_report_by_id(
    report_id="DiagnosticReport/77777"
)
```

## Advanced Search Patterns

### Date Range Queries

FHIR supports several date prefixes for range queries:

- `eq` - Equal to (default if no prefix)
- `ne` - Not equal to
- `gt` - Greater than
- `ge` - Greater than or equal to
- `lt` - Less than
- `le` - Less than or equal to

```python
# Get observations from the last 30 days
observations = await get_patient_observations(
    patient_id="12345",
    date="ge2024-10-20"
)

# Get procedures before a specific date
procedures = await get_patient_procedures(
    patient_id="12345",
    date="lt2024-01-01"
)
```

### Combining Multiple Queries

```python
# Build a comprehensive patient summary
patient_id = "12345"

# Get patient demographics
patient = await get_patient_by_id(patient_id)

# Get active medical conditions
conditions = await get_patient_conditions(
    patient_id=patient_id
    clinical_status="active"
)

# Get active allergies
allergies = await get_patient_allergies(
    patient_id=patient_id
    clinical_status="active"
)

# Get active medications
medications = await get_patient_medication_requests(
    patient_id=patient_id
    status="active"
)

# Get recent vital signs
vitals = await get_patient_vital_signs(
    patient_id=patient_id
    date="ge2024-10-01"
)

# Get upcoming appointments
appointments = await get_patient_appointments(
    patient_id=patient_id
    date="ge2024-11-19",
    status="booked"
)
```

### Server Capabilities

```python
# Get FHIR server capabilities and metadata
capabilities = await get_fhir_capability_statement()

# This returns information about:
# - Supported FHIR resources
# - Available search parameters
# - Supported operations
# - Server version and configuration
```

## Error Handling

When using the tools, handle potential errors gracefully:

```python
try:
    patient = await get_patient_by_id(patient_id="12345")
except httpx.HTTPStatusError as e:
    if e.response.status_code == 404:
        print("Patient not found")
    elif e.response.status_code == 401:
        print("Authentication failed - check your OAuth token")
    elif e.response.status_code == 403:
        print("Access denied - insufficient permissions")
    else:
        print(f"Error: {e.response.status_code} - {e.response.text}")
```

## Tips and Best Practices

1. **Filter Early**: Use status and date filters to reduce data volume and improve query performance
2. **Patient ID Format**: Some FHIR servers require the full reference format (e.g., "Patient/12345"), others accept just the ID ("12345")
3. **Date Formats**: Use ISO 8601 format (YYYY-MM-DD) for dates
4. **Date Range Operators**: Use FHIR search operators like `ge` (greater than or equal), `le` (less than or equal), `gt`, `lt` for date ranges
5. **Test with Capabilities**: Check server capabilities first using `get_fhir_capability_statement()` to understand what's supported
6. **Handle Empty Results**: Always check if search results contain entries before processing
7. **Respect Rate Limits**: Be mindful of API rate limits when making multiple requests
8. **Use Specific Searches**: Use the most specific search method available (e.g., search by identifier rather than name when possible)

## Resources

- [FHIR R4 Specification](https://hl7.org/fhir/R4/)
- [FHIR Search Parameters](https://hl7.org/fhir/R4/search.html)
- [Oracle Millennium Platform API Documentation](https://docs.oracle.com/en/industries/health/millennium-platform-apis/)
