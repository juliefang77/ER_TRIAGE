from rest_framework import serializers
from datetime import datetime, timedelta
from django.utils import timezone

# Date range validation, default to last month
class DateRangeSerializer(serializers.Serializer):
    
    def get_default_start_date():
        # Get first day of previous month
        today = timezone.now()
        first_of_this_month = today.replace(day=1)
        last_month = first_of_this_month - timedelta(days=1)
        return last_month.replace(day=1)

    def get_default_end_date():
        # Get last day of previous month
        today = timezone.now()
        first_of_this_month = today.replace(day=1)
        return first_of_this_month - timedelta(days=1)

    start_date = serializers.DateField(
        required=False,
        default=get_default_start_date
    )
    end_date = serializers.DateField(
        required=False,
        default=get_default_end_date
    )

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("结束日期必须晚于开始日期")
        return data


# Standardize response format to the frontend
class DistributionResponseSerializer(serializers.Serializer):
    labels = serializers.ListField(child=serializers.CharField())
    data = serializers.ListField(child=serializers.IntegerField())
    total = serializers.IntegerField()
    percentages = serializers.ListField(child=serializers.FloatField())