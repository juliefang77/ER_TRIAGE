from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Patient, TriageRecord, VitalSigns
from .serializers import (
    PatientSerializer, 
    TriageRecordSerializer,
    VitalSignsSerializer
)

class PatientAppPatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def create(self, request):
        patient_serializer = PatientSerializer(data={
            'id_type': request.data.get('id_type'),
            'id_number': request.data.get('id_number'),
            'name_chinese': request.data.get('name_chinese')
        })
        if patient_serializer.is_valid():
            patient = patient_serializer.save()
            return Response(patient_serializer.data, status=status.HTTP_201_CREATED)
        return Response(patient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientAppTriageViewSet(viewsets.ModelViewSet):
    queryset = TriageRecord.objects.all()
    serializer_class = TriageRecordSerializer

    def create(self, request):
        triage_serializer = TriageRecordSerializer(data={
            'patient': request.data.get('patient'),
            'chief_complaint': request.data.get('chief_complaint'),
            'priority_level': 4,
            'area': 'GREEN',
            'status': 'WAITING'
        })
        if triage_serializer.is_valid():
            triage = triage_serializer.save()
            return Response(triage_serializer.data, status=status.HTTP_201_CREATED)
        return Response(triage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientAppVitalSignsViewSet(viewsets.ModelViewSet):
    queryset = VitalSigns.objects.all()
    serializer_class = VitalSignsSerializer

    def create(self, request):
        vitals_serializer = VitalSignsSerializer(data={
            'triage_record': request.data.get('triage_record'),
            'temperature': request.data.get('temperature'),
            'pain_score': request.data.get('pain_score')
        })
        if vitals_serializer.is_valid():
            vitals = vitals_serializer.save()
            return Response(vitals_serializer.data, status=status.HTTP_201_CREATED)
        return Response(vitals_serializer.errors, status=status.HTTP_400_BAD_REQUEST)