from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PendingSubmissionViewSet, PendingSubmissionDataViewSet, PatientTriageSubmissionViewSet
# Authentication
from django.urls import path
from .views.patient import request_login, verify_code

router = DefaultRouter()

# Patient submit form: /apipatient/patientsubmissions/
router.register(r'patientsubmissions', PatientTriageSubmissionViewSet)

# list all pending submitted forms: /apipatient/pendingsubmissions/
router.register(r'pendingsubmissions', PendingSubmissionViewSet, basename='pending-submissions')

# get submission data for auto fill: apipatient/autofilltriage/{patient id, which you get from previous API}
router.register(r'autofilltriage', PendingSubmissionDataViewSet, basename='autofill-triage')  

urlpatterns = [
    path('', include(router.urls)),
    path('login/', request_login, name='patient-login'),
    path('verify/', verify_code, name='patient-verify'),
]