from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .apipatient import PendingSubmissionViewSet, PendingSubmissionDataViewSet, PatientTriageSubmissionViewSet

router = DefaultRouter()

# Patient submit form: /apipatient/patientsubmissions/
router.register(r'patientsubmissions', PatientTriageSubmissionViewSet)

# list all pending submitted forms: /apipatient/pendingsubmissions/
router.register(r'pendingsubmissions', PendingSubmissionViewSet, basename='pending-submissions')

# get submission data for auto fill: apipatient/autofilltriage/{patient id, which you get from previous API}
router.register(r'autofilltriage', PendingSubmissionDataViewSet, basename='autofill-triage')  

urlpatterns = [
    path('', include(router.urls)),
]