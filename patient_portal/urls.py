from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    register, verify_registration, login,
    PatientTriageSubmissionViewSet,
    PendingSubmissionViewSet,
    PendingSubmissionDataViewSet,
    PatientSurveyViewSet,
    PatientMessageViewSet
)
# Authentication
from django.urls import path

router = DefaultRouter()

# APP API: Patient submit form: /apipatient/patientsubmissions/
router.register(r'patientsubmissions', PatientTriageSubmissionViewSet)

# SaaS API: list all pending submitted forms: /apipatient/pendingsubmissions/
router.register(r'pendingsubmissions', PendingSubmissionViewSet, basename='pending-submissions')

# SaaS API: get submission data for auto fill: apipatient/autofilltriage/{patient id, which you get from previous API}
router.register(r'autofilltriage', PendingSubmissionDataViewSet, basename='autofill-triage')  

# APP API: Patient gets survey 
router.register(r'surveys', PatientSurveyViewSet, basename='patient-surveys')

# APP API: Patient gets messages
router.register(r'messages', PatientMessageViewSet, basename='patient-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register, name='patient-register'),
    path('verify/', verify_registration, name='patient-verify'),
    path('login/', login, name='patient-login'),
]