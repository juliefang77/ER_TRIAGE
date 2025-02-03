from django.db.models import Count
from django.db.models.functions import TruncDate
from triage.models import TriageRecord, TriageResult, HospitalUser, Hospital
from datetime import datetime, time
from django.utils import timezone

class PatientDistributionStats:
    def __init__(self, queryset, start_date=None, end_date=None):
        self.queryset = queryset.select_related('result')
        
        print("1. Initial queryset count:", self.queryset.count())
        
        # Simplified date filtering - just use the date strings directly
        if start_date:
            self.queryset = self.queryset.filter(registration_time__gte=start_date)
        if end_date:
            self.queryset = self.queryset.filter(registration_time__lte=end_date)
            
        print("2. After date filter count:", self.queryset.count())
        self.total_patients = self.queryset.count()
              
    def get_priority_level_distribution(self):
        # Add debug print of raw query
        distribution_query = self.queryset.select_related('result')\
            .values('result__priority_level')\
            .annotate(count=Count('id'))

        distribution = distribution_query.order_by('result__priority_level')
    
        priority_levels = ['一级', '二级', '三级', '四级']
        counts = [0] * 4
        percentages = [0.0] * 4
        total = 0
    
        for item in distribution:
            level = item['result__priority_level']
            count = item['count']
            if level is not None:  # Only process non-null levels
                level_index = level - 1  # Convert level (1-4) to index (0-3)
                counts[level_index] = count
                total += count
    
        final_result = {
            'labels': priority_levels,
            'data': counts,
            'total': total,
            'percentages': [(count/total)*100 if total > 0 else 0 for count in counts]
        }
        print("4. Final result:", final_result)
        return final_result
         
    
    def get_department_distribution(self):
        distribution = self.queryset.select_related('result')\
            .values('result__department')\
            .annotate(count=Count('id'))\
            .order_by('result__department')

        # Use dictionary to consolidate departments
        dept_counts = {}
        total = 0

        # Process results and combine duplicates
        for item in distribution:
            dept = item['result__department'] or '未分类'  # Handle null/empty as '未分类'
            count = item['count']
            # Add to existing count or create new entry
            dept_counts[dept] = dept_counts.get(dept, 0) + count
            total += count

        # Convert to sorted lists
        departments = list(dept_counts.keys())
        counts = [dept_counts[dept] for dept in departments]
        percentages = [(count / total * 100) if total > 0 else 0 for count in counts]

        return {
            'labels': departments,
            'data': counts,
            'total': total,
            'percentages': percentages
        }
