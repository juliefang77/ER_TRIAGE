from rest_framework import serializers
from triage.models import Hospital

# First, create a new serializer for the message-patient pair
class MessageRecipientSerializer(serializers.Serializer):
    triage_record_id = serializers.IntegerField()
    content = serializers.CharField()

class MassSendMessageSerializer(serializers.Serializer):
    messages = MessageRecipientSerializer(many=True)


# 给 frontend 医院名称
class HospitalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'name']