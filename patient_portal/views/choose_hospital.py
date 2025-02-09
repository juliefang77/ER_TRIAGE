from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from triage.models import Hospital
from rest_framework import serializers

# Create a custom pagination class
class HospitalPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

# Serializer
class HospitalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'name', 'address', 'city', 'district', 'level']

# Patient views hospital list, and chooses one to book
class HospitalListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hospital.objects.filter(is_active=True).order_by('id')
    serializer_class = HospitalListSerializer
    permission_classes = [AllowAny]
    authentication_classes = []  # No authentication required
    pagination_class = HospitalPagination