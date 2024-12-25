from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from . import apisaas
from . import apipatient 

router = DefaultRouter()

# SaaS endpoints with apisaas prefix
# Remove apisaas prefix from here since it's in config/urls.py
router.register(r'patients', apisaas.SaaSPatientViewSet, basename='saas-patient')
router.register(r'triage', apisaas.SaaSTriageViewSet, basename='saas-triage') # use this only
router.register(r'vitals', apisaas.SaaSVitalSignsViewSet, basename='saas-vitals')
router.register(r'staff', apisaas.SaaSMedicalStaffViewSet, basename='saas-staff')

# SaaS: New endpoints for triage results and history
router.register(r'triageresults', apisaas.SaaSTriageResultViewSet, basename='saas-triage-results')

# Patient app endpoints
router_patient = DefaultRouter()
router_patient.register(r'patients', apipatient.PatientAppPatientViewSet, basename='app-patient')
router_patient.register(r'triage', apipatient.PatientAppTriageViewSet, basename='app-triage')
router_patient.register(r'vitals', apipatient.PatientAppVitalSignsViewSet, basename='app-vitals')

urlpatterns = [
    path('', include(router.urls)),
    path('apipatient/', include(router_patient.urls)),
]

