from rest_framework import viewsets, permissions
from rest_framework.response import Response
from triage.models import HospitalFeedback
from triage.serializers.feedback_serializer import HospitalFeedbackSerializer

class HospitalFeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = HospitalFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Filter feedbacks to only show those submitted by the current hospital user
        return HospitalFeedback.objects.filter(hospital_user=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set the hospital_user when creating feedback
        serializer.save(hospital_user=self.request.user)