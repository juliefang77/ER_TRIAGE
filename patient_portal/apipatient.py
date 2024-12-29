from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Patient
from .patient_serializer import PatientSelfRegistrationSerializer

class PatientSelfRegistrationViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]  # Allow unauthenticated access
    serializer_class = PatientSelfRegistrationSerializer
    
    def get_queryset(self):
        # If patient is viewing records (GET request)
        if self.request.method == 'GET':
            id_number = self.request.query_params.get('id_number')
            if not id_number:
                return Patient.objects.none()  # Return empty if no ID provided
                
            return Patient.objects.filter(
                id_number=id_number
            ).prefetch_related(
                'triage_records',
                'triage_records__result',
                'triage_records__vital_signs'
            )
        
        # For other methods (POST/create), return empty queryset
        return Patient.objects.none()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()

        return Response({
            'message': '您已成功提交分诊信息',
            'patient_id': patient.id,
            'id_number': patient.id_number  # Also return ID number for reference
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        # Custom retrieve to verify ID number
        id_number = request.query_params.get('id_number')
        if not id_number:
            return Response({
                'error': '请提供身份证号码'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            patient = Patient.objects.get(id_number=id_number)
            serializer = self.get_serializer(patient)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response({
                'error': '未找到病人记录'
            }, status=status.HTTP_404_NOT_FOUND)