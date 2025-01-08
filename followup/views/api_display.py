from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from triage.models import TriageRecord
from ..models import FollowupRecipient
from ..serializers.recorddisplay_serializer import FollowupTriageRecordSerializer

# For displaying records
class FollowupRecordDisplayViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FollowupTriageRecordSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return TriageRecord.objects.filter(
            hospital=self.request.user
        ).select_related(
            'patient',
            'nurse',
            'hospital',
            'recipient',
            'result'
        )

