from ..serializers.ercompanion_serializer import ErCompanionSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from ..models import ErCompanion
from .auth import PatientTokenAuthentication

class ErCompanionViewSet(viewsets.ModelViewSet):
    serializer_class = ErCompanionSerializer
    authentication_classes = [PatientTokenAuthentication]

    def get_queryset(self):
        return ErCompanion.objects.filter(patient_user=self.request.user)

    def perform_create(self, serializer):
        # Creates new ErCompanion instance with the authenticated patient_user
        serializer.save(patient_user=self.request.user)