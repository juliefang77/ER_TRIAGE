from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from followup.serializers.message_serializer import MassSendMessageSerializer
from followup.models import FollowupMessage, FollowupRecipient
from triage.models import TriageRecord

class MassSendMessageViewSet(viewsets.ViewSet):
    """ViewSet for mass sending messages to patients"""
    serializer_class = MassSendMessageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def send(self, request):
        """Send customized message to selected patients"""
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        triage_record_ids = serializer.validated_data['triage_record_ids']
        content = serializer.validated_data['content']

        messages_created = []
        for record_id in triage_record_ids:
            # Get or create recipient
            recipient, _ = FollowupRecipient.objects.get_or_create(
                triage_record_id=record_id,
                hospital=request.user,
                defaults={
                    'patient': TriageRecord.objects.get(id=record_id).patient,
                    'patient_user': TriageRecord.objects.get(id=record_id).patient.patient_user
                }
            )

            # Create message record
            message = FollowupMessage.objects.create(
                hospital=request.user,
                recipient=recipient,
                content=content
            )
            messages_created.append(message)

            # Update recipient status
            recipient.message_reply = 'SENT'
            recipient.save()

            # TODO: Send app notification to patient_user if exists
            # This would integrate with your notification system

        return Response({
            "message": f"Successfully sent message to {len(messages_created)} patients",
            "messages_created": len(messages_created)
        }, status=status.HTTP_201_CREATED)