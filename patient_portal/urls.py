from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    register, verify_registration, login,
    PatientTriageSubmissionViewSet,
    PendingSubmissionViewSet,
    PendingSubmissionDataViewSet,
    PatientSurveyViewSet  # Add this import
)
# Authentication
from django.urls import path

router = DefaultRouter()

# Patient submit form: /apipatient/patientsubmissions/
router.register(r'patientsubmissions', PatientTriageSubmissionViewSet)

# list all pending submitted forms: /apipatient/pendingsubmissions/
router.register(r'pendingsubmissions', PendingSubmissionViewSet, basename='pending-submissions')

# get submission data for auto fill: apipatient/autofilltriage/{patient id, which you get from previous API}
router.register(r'autofilltriage', PendingSubmissionDataViewSet, basename='autofill-triage')  

# Patient gets survey 
router.register(r'surveys', PatientSurveyViewSet, basename='patient-surveys')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register, name='patient-register'),
    path('verify/', verify_registration, name='patient-verify'),
    path('login/', login, name='patient-login'),
]