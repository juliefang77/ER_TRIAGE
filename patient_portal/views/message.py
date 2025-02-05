from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from patient_portal.serializers.message_serializer import PatientMessageSerializer, MessageReplySerializer
from rest_framework.permissions import AllowAny
from followup.models import FollowupMessage
from django.utils import timezone

class PatientMessageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PatientMessageSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        phone = self.request.query_params.get('phone')
        if not phone:
            return FollowupMessage.objects.none()
        
        return FollowupMessage.objects.filter(
            recipient__patient_user__phone=phone,  # Direct to patient_user
            # recipient__message_reply='SENT'  # Show all messages
        ).select_related('hospital', 'recipient')

    @action(detail=True, methods=['post'])
    def submit_reply(self, request, pk=None):
        message = self.get_object()
        
        if message.recipient.message_reply not in ['SENT', 'NOT_SENT']:
            return Response(
                {"error": "Already replied to this message"},
                status=status.HTTP_400_BAD_REQUEST
            )

        reply_serializer = MessageReplySerializer(data=request.data)
        if reply_serializer.is_valid():
            # Update recipient with reply choice
            recipient = message.recipient
            recipient.message_reply = reply_serializer.validated_data['reply_time']
            recipient.save()

            # Update message timestamp
            message.responded_at = timezone.now()
            message.save()

            return Response({"message": "Reply submitted successfully"})
        
        return Response(
            reply_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    