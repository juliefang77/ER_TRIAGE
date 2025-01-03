from django.db.models import Count
from django.db.models.functions import TruncDate
from triage.models import TriageRecord, TriageResult, HospitalUser, Hospital
from datetime import datetime

class PatientDistributionStats:
    def __init__(self, queryset, start_date=None, end_date=None):
        # param hospital: HospitalUser instance from request.user.hospital
        # param start_date: YYYY-MM-DD string
        # @param end_date: YYYY-MM-DD string

        # Handle both Hospital and HospitalUser instances
        self.queryset = queryset
        
        if start_date and end_date:
            self.queryset = self.queryset.filter(
                registration_time__date__range=[start_date, end_date]
            )
            
        self.total_patients = self.queryset.count()


    def get_priority_level_distribution(self):
        # 获取急诊患者分级分布 based on registration_time
        # Only counting patients with assigned priority levels
        distribution = self.queryset.select_related('result')\
            .exclude(result__priority_level__isnull=True)\
            .values('result__priority_level')\
            .annotate(count=Count('id'))\
            .order_by('result__priority_level')

        level_counts = {
            item['result__priority_level']: item['count']
            for item in distribution 
        }

        labels = []
        data = []

        # Only process assigned priority levels
        for level_num, level_name in TriageResult.PRIORITY_LEVELS:
            labels.append(level_name)
            count = level_counts.get(level_num, 0)
            data.append(count)

        # Calculate total of only assigned patients
        total_assigned = sum(data)

        # Calculate percentages based only on assigned patients
        percentages = [
            round((count / total_assigned * 100), 1) 
            if total_assigned > 0 else 0
            for count in data
        ]

        return {
            'labels': labels,  # Will contain: ['一级', '二级', '三级', '四级']
            'data': data,
            'total': total_assigned,  # Only counts patients with priority levels
            'percentages': percentages
        }
    
    
    def get_department_distribution(self):
        # 科室分布
        distribution = self.queryset.select_related('result')\
            .exclude(result__department__isnull=True)\
            .exclude(result__department='')\
            .values('result__department')\
            .annotate(count=Count('id'))\
            .order_by('result__department')

        # Create a dictionary mapping department codes to their counts
        dept_counts = {
            item['result__department']: item['count']
            for item in distribution
        }

        labels = []
        data = []

        # Process all predefined departments
        for dept_code, dept_name in TriageResult.DEPARTMENT_CHOICES:
            labels.append(dept_name)
            count = dept_counts.get(dept_code, 0)
            data.append(count)

        # Calculate total of only assigned patients
        total_assigned = sum(data)

        # Calculate percentages based only on assigned patients
        percentages = [
            round((count / total_assigned * 100), 1) 
            if total_assigned > 0 else 0
            for count in data
        ]

        return {
            'labels': labels,  # Will contain Chinese department names
            'data': data,
            'total': total_assigned,
            'percentages': percentages
        }
    
