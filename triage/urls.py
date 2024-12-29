from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from . import apisaas
from .apisaas import CustomAuthToken  # Add this import

router = DefaultRouter()

# SaaS endpoints with apisaas prefix
router.register(r'patients', apisaas.SaaSPatientViewSet, basename='saas-patient')
router.register(r'triage', apisaas.SaaSTriageViewSet, basename='saas-triage') # use this only
router.register(r'vitals', apisaas.SaaSVitalSignsViewSet, basename='saas-vitals')
router.register(r'staff', apisaas.SaaSMedicalStaffViewSet, basename='saas-staff')

# SaaS: No longer used
router.register(r'triagehistory', apisaas.TriageHistoryViewSet, basename='triage-history')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomAuthToken.as_view(), name='api_token'),
]

