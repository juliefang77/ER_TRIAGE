from rest_framework import serializers
from django.utils import timezone
from datetime import datetime, time, timedelta

# Date range validation, default to last month
class DateRangeSerializer(serializers.Serializer):
    start_date = serializers.CharField(
        required=False,
        default=lambda: (
            timezone.now() - timedelta(days=30)
        ).strftime('%Y-%m-%d')
    )
    
    end_date = serializers.CharField(
        required=False,
        default=lambda: timezone.now().strftime('%Y-%m-%d')
    )


# Standardize response format to the frontend
class DistributionResponseSerializer(serializers.Serializer):
    labels = serializers.ListField(child=serializers.CharField())
    data = serializers.ListField(child=serializers.IntegerField())
    total = serializers.IntegerField()
    percentages = serializers.ListField(child=serializers.FloatField())
