# patient_portal/models/__init__.py
from .patient_user import PatientUser
from .patient_triage import PatientTriageSubmission

__all__ = ['PatientUser', 'PatientTriageSubmission']