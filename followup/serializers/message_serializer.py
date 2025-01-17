from rest_framework import serializers

class MassSendMessageSerializer(serializers.Serializer):
    triage_record_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True
    )
    content = serializers.CharField(required=True)