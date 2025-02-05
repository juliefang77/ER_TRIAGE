from rest_framework import serializers
from followup.models import FollowupMessage
from triage.models import Hospital

class MessageReplySerializer(serializers.Serializer):
    reply_time = serializers.ChoiceField(
        choices=[
            ('WEEKEND', '周末'),
            ('WEEK_DAY', '周中白天'),
            ('WEEK_NIGHT', '周中晚上'),
            ('ANYTIME', '任意时间')
        ],  # Only valid reply choices, excluding SENT/NOT_SENT
        required=True
    )

class PatientMessageSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(source='hospital.name')

    class Meta:
        model = FollowupMessage
        fields = ['id', 'content', 'sent_at', 'responded_at', 'hospital_name']

