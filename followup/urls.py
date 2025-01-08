from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import FollowupRecordDisplayViewSet, AddToFollowupViewSet

router = DefaultRouter()

# Register without the apifollowup prefix since it's handled in global urls.py
router.register(
    r'display', FollowupRecordDisplayViewSet, basename='saas-followup-display')


router.register(
    r'management', AddToFollowupViewSet, basename='saas-followup-management')

urlpatterns = [
    path('', include(router.urls)),
]