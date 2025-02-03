from rest_framework import viewsets, status
from rest_framework.response import Response  # Add this import
from ..models import MassInjury
from django.db.models import Count
from ..serializers.mass_serializer import MassInjurySerializer, MassInjuryCreateSerializer
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from django.db.models import Count, Q

class MassInjuryFilter(filters.FilterSet):
    # Date filters for mass_time (using CharFilter like your example)
    start_date = filters.CharFilter(field_name='mass_time', lookup_expr='gte')
    end_date = filters.CharFilter(field_name='mass_time', lookup_expr='lte')
    
    # Mass type filter with choices
    mass_type = filters.ChoiceFilter(
        choices=MassInjury.MASS_TYPE_CHOICES
    )
    
    # Mass name filter with partial matching
    mass_name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = MassInjury
        fields = ['start_date', 'end_date', 'mass_type', 'mass_name']

# Add a pagination class (you can put this at the top of your file)
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class MassInjuryViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination  # Add this line
    filterset_class = MassInjuryFilter  # Add this line
    filter_backends = [DjangoFilterBackend]  # Add this line

    def get_serializer_class(self):
        if self.action == 'create':
            return MassInjuryCreateSerializer
        return MassInjurySerializer

    def get_queryset(self):
        return MassInjury.objects.filter(
            hospital=self.request.user.hospital  # Filter by current hospital user
        ).annotate(
            mass_triaged=Count('triage_records')
        ).order_by('-mass_time')

    def perform_create(self, serializer):
        """Automatically set hospital to current user"""
        serializer.save(hospital=self.request.user.hospital)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Fetch the created instance with annotated mass_triaged
        instance = self.get_queryset().get(id=serializer.instance.id)
        read_serializer = MassInjurySerializer(instance)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)
    