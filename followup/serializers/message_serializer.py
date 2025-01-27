from rest_framework import serializers

# First, create a new serializer for the message-patient pair
class MessageRecipientSerializer(serializers.Serializer):
    triage_record_id = serializers.IntegerField()
    content = serializers.CharField()

class MassSendMessageSerializer(serializers.Serializer):
    messages = MessageRecipientSerializer(many=True)