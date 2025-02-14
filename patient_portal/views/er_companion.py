from ..serializers.ercompanion_serializer import ErCompanionSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from ..models import ErCompanion
from .auth import PatientTokenAuthentication
from rest_framework.decorators import action

class ErCompanionViewSet(viewsets.ModelViewSet):
    serializer_class = ErCompanionSerializer
    authentication_classes = [PatientTokenAuthentication]

    def get_queryset(self):
        return ErCompanion.objects.filter(patient_user=self.request.user)

    def perform_create(self, serializer):
        # Creates new ErCompanion instance with the authenticated patient_user
        serializer.save(patient_user=self.request.user)

    # Track 患者到了哪一步
    @action(detail=True, methods=['post'])
    def increment_step(self, request, pk=None):
        companion = self.get_object()
        if companion.last_completed_step is None:
            companion.last_completed_step = 1
        else:
            companion.last_completed_step += 1
        companion.save()
        return Response({'last_completed_step': companion.last_completed_step})