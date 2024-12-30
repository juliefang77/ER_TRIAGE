from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .apipatient import PendingSubmissionViewSet, PendingSubmissionDataViewSet

router = DefaultRouter()

# list all pending submitted forms
router.register(r'pendingsubmissions', PendingSubmissionViewSet, basename='pending-submissions')

# get submission data for auto fill
router.register(r'autofilltriage', PendingSubmissionDataViewSet, basename='autofill-triage')  # Changed to ViewSet

urlpatterns = [
    path('', include(router.urls)),
]