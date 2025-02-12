from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PatientTriageSubmissionViewSet,
    PendingSubmissionViewSet,
    PendingSubmissionDataViewSet,
    PatientSurveyViewSet,
    PatientMessageViewSet,
    BookingViewSet,
    HospitalBookingViewSet,
    PatientSurveyListViewSet,
    PatientAuthToken,
    PatientRegisterView,
    PatientVerifyView,
    AuthenticatedPatientTriageSubmissionViewSet,
    PatientHistoricalSurveyListViewSet,
    HospitalListViewSet,
    ErCompanionViewSet,
)
# Authentication
from django.urls import path

router = DefaultRouter()

# APP API: Patient submit form: /apipatient/patientsubmissions/
router.register(r'patientsubmissions', PatientTriageSubmissionViewSet)

# APP API: Logged in patient submits triage form
router.register(r'authenticated-patient-submissions', AuthenticatedPatientTriageSubmissionViewSet, 
    basename='authenticated-patient-submissions')  # Added unique basename

# SaaS API: list all pending submitted forms: /apipatient/pendingsubmissions/
router.register(r'pendingsubmissions', PendingSubmissionViewSet, basename='pending-submissions')

# SaaS API: get submission data for auto fill: apipatient/autofilltriage/{patient id, which you get from previous API}
router.register(r'autofilltriage', PendingSubmissionDataViewSet, basename='autofill-triage')  

# APP API: Patient gets survey list (light API)
router.register(r'patient-surveys-list', PatientSurveyListViewSet, basename='patient-surveys-list')

# APP API: Patient historical survey list (light API)
router.register(
    r'patient-historical-surveys-list', 
    PatientHistoricalSurveyListViewSet, 
    basename='patient-historical-surveys-list'
)

# APP API: Patient gets survey (detail view & submission)
router.register(r'surveys', PatientSurveyViewSet, basename='patient-surveys')

# APP API: Patient gets messages
router.register(r'messages', PatientMessageViewSet, basename='patient-messages')

# APP API: Patient views hospital list, and chooses one to book from
router.register(r'view-hospitals', HospitalListViewSet, basename='view-hospitals-list')

# APP API: Patient makes booking and views bookings
router.register(r'bookings', BookingViewSet, basename='patient-bookings')

# SaaS API: Hospital views bookings list 
router.register(r'hospital-bookings', HospitalBookingViewSet, basename='hospital-booking')

# APP API: ER companion 付费小莲花
router.register(r'er-companion', ErCompanionViewSet, basename='er-companion')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', PatientRegisterView.as_view(), name='patient-register'),
    path('verify/', PatientVerifyView.as_view(), name='patient-verify'),
    path('token/', PatientAuthToken.as_view(), name='patient-token'),
]