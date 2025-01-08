from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from triage.models import TriageRecord
from ..models import FollowupRecipient
from ..serializers.recorddisplay_serializer import FollowupTriageRecordSerializer
from django.db.models import Exists, OuterRef

# For displaying records
class FollowupRecordDisplayViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FollowupTriageRecordSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Create subquery for followup check
        followup_exists = FollowupRecipient.objects.filter(
            triage_record=OuterRef('pk'),
            hospital=self.request.user  # Filter by hospital
        )

        return TriageRecord.objects.filter(
            hospital=self.request.user
        ).select_related(
            'patient',
            'nurse',
            'hospital',
            'recipient',
            'result'
        ).annotate(
            has_followup=Exists(followup_exists)
        )

