from django.urls import path, include
from rest_framework.routers import DefaultRouter
from patient_portal import apipatient  # Import the module like in triage/urls.py

router = DefaultRouter()
router.register(
    'register', 
    apipatient.PatientSelfRegistrationViewSet,  # Use the correct ViewSet name
    basename='patient-registration'
)

urlpatterns = [
    path('', include(router.urls)),
]