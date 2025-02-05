from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from followup.serializers.message_serializer import MassSendMessageSerializer, HospitalInfoSerializer
from followup.models import FollowupMessage, FollowupRecipient
from triage.models import TriageRecord
from django.db import transaction
from rest_framework import serializers

# 群发消息，邀请患者随访，并填写方便的时间
class MassSendMessageViewSet(viewsets.ViewSet):
    """ViewSet for mass sending messages to patients"""
    serializer_class = MassSendMessageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def send(self, request):
        """Send different messages to different patients"""
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        messages_data = serializer.validated_data['messages']
        
        try:
            with transaction.atomic():  # Use transaction to ensure all operations succeed or none do
                messages_created = []
                for message_data in messages_data:
                    record_id = message_data['triage_record_id']
                    content = message_data['content']

                    # Get or create recipient
                    try:
                        triage_record = TriageRecord.objects.get(id=record_id)
                        recipient, _ = FollowupRecipient.objects.get_or_create(
                            triage_record_id=record_id,
                            hospital=request.user.hospital,
                            defaults={
                                'patient': triage_record.patient,
                                'patient_user': triage_record.patient.patient_user
                            }
                        )

                        # Create message record
                        message = FollowupMessage.objects.create(
                            hospital=request.user.hospital,
                            recipient=recipient,
                            content=content
                        )
                        messages_created.append(message)

                        # Update recipient status
                        recipient.message_reply = 'SENT'
                        recipient.save()

                        # TODO: Send app notification to patient_user if exists

                    except TriageRecord.DoesNotExist:
                        raise serializers.ValidationError(
                            f"Triage record with id {record_id} does not exist"
                        )

                return Response({
                    "message": f"Successfully sent {len(messages_created)} messages",
                    "messages_created": len(messages_created)
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

# Frontend gets hospital name
class HospitalUserViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def my_hospital(self, request):
        """Get current user's affiliated hospital"""
        if not request.user.is_authenticated:
            return Response({'error': '请先登录'}, status=401)
            
        if not request.user.hospital:
            return Response({'error': '用户未关联医院'}, status=404)
            
        serializer = HospitalInfoSerializer(request.user.hospital)
        return Response(serializer.data)