from rest_framework import serializers
from django.utils import timezone
from datetime import datetime, time, timedelta

# Date range validation, default to last month
class DateRangeSerializer(serializers.Serializer):
    
    start_date = serializers.DateField(
        required=False, 
        default=lambda: datetime.combine(
            (timezone.now() - timedelta(days=30)).date(), 
            time.min
        )
    )
    end_date = serializers.DateField(
        required=False, 
        default=lambda: datetime.combine(
            timezone.now().date(), 
            time.max
        )
    )


# Standardize response format to the frontend
class DistributionResponseSerializer(serializers.Serializer):
    labels = serializers.ListField(child=serializers.CharField())
    data = serializers.ListField(child=serializers.IntegerField())
    total = serializers.IntegerField()
    percentages = serializers.ListField(child=serializers.FloatField())
