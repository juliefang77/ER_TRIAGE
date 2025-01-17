from rest_framework.routers import DefaultRouter
from django.urls import path, include
from triage.views import CustomAuthToken
from .views import CustomAuthToken  # Add this import
from triage.views import (
    SaaSTriageViewSet,
    SaaSMedicalStaffViewSet,
    TriageHistoryViewSet,
    SaaSPatientViewSet,
    TriageHistoryListViewSet
)

router = DefaultRouter()

# 提交分诊表
router.register(r'triage', SaaSTriageViewSet, basename='saas-triage') 

# Not used
router.register(r'staff', SaaSMedicalStaffViewSet, basename='saas-staff')
router.register(r'patients', SaaSPatientViewSet, basename='saas-patient')

# Used for 分诊记录
router.register(r'triagehistory/list', TriageHistoryListViewSet, basename='triage-history-list')  # List view (simplified)
router.register(r'triagehistory', TriageHistoryViewSet, basename='triage-history')  # Detail view (comprehensive)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomAuthToken.as_view(), name='api_token'),
]

