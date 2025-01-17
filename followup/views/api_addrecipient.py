from rest_framework import viewsets
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from triage.models import TriageRecord
from ..models import FollowupRecipient

class AddToFollowupViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def add_patients(self, request):
        triage_record_ids = request.data.get('triage_record_ids', [])
        
        if not triage_record_ids:
            return Response(
                {"error": "No triage records selected"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get triage records that don't already have followup recipients
        triage_records = TriageRecord.objects.filter(
            id__in=triage_record_ids,
            hospital=self.request.user
        ).exclude(
            recipient__isnull=False
        )

        # Bulk create followup recipients
        recipients_to_create = [
            FollowupRecipient(
                patient=record.patient,
                hospital=record.hospital,
                triage_record=record,
                patient_user=record.patient.patient_user if hasattr(record.patient, 'patient_user') else None, 
                survey_status= 'default',
                call_status='default'
            ) for record in triage_records
        ]

        created_recipients = FollowupRecipient.objects.bulk_create(recipients_to_create)

        return Response({
            "message": f"Successfully added {len(created_recipients)} patients to followup plan",
            "created_count": len(created_recipients)
        }, status=status.HTTP_201_CREATED)