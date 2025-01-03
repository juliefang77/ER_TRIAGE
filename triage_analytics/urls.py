from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views.patient_views import PatientStatsViewSet

router = DefaultRouter()

# Register viewset with 'apichart' prefix
router.register(r'patientstats', PatientStatsViewSet, basename='chart-patient')


urlpatterns = router.urls