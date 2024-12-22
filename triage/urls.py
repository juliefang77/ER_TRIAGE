from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from . import apisaas

router = DefaultRouter()

# SaaS endpoints with apisaas prefix
# Remove apisaas prefix from here since it's in config/urls.py
router.register(r'patients', apisaas.SaaSPatientViewSet, basename='saas-patient')
router.register(r'triage', apisaas.SaaSTriageViewSet, basename='saas-triage')
router.register(r'vitals', apisaas.SaaSVitalSignsViewSet, basename='saas-vitals')
router.register(r'staff', apisaas.SaaSMedicalStaffViewSet, basename='saas-staff')

urlpatterns = router.urls
