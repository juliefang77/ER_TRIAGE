from rest_framework import viewsets, status
from rest_framework.response import Response  # Add this import
from ..models import MassInjury
from django.db.models import Count
from ..serializers.mass_serializer import MassInjurySerializer, MassInjuryCreateSerializer

class MassInjuryViewSet(viewsets.ModelViewSet):
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
    