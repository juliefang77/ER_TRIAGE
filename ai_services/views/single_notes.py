from rest_framework import viewsets
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from followup.models import FollowupNotetaking
from triage.models import Patient
from ..services.baidu_service import BaiduAIService
from ..serializers.notes_serializer import AiNotesListSerializer

from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters

class AiNotesPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# 随访中，查看保存笔记页面
class AiNotesFilter(filters.FilterSet):
    # Date range filters for created_at
    created_at_start = filters.CharFilter(field_name='created_at', lookup_expr='gte')
    created_at_end = filters.CharFilter(field_name='created_at', lookup_expr='lte')
    
    # Patient name and phone filters (through foreign key)
    name_patient = filters.CharFilter(field_name='patient__name_patient', lookup_expr='icontains')
    patient_phone = filters.CharFilter(field_name='patient__patient_phone', lookup_expr='icontains')

    class Meta:
        model = FollowupNotetaking
        fields = ['created_at_start', 'created_at_end', 'name_patient', 'patient_phone']

class AiNotesListViewSet(viewsets.ModelViewSet):
    serializer_class = AiNotesListSerializer
    pagination_class = AiNotesPagination
    filterset_class = AiNotesFilter
    search_fields = ['patient__name_patient', 'patient__patient_phone']

    def get_queryset(self):
        return FollowupNotetaking.objects.filter(
            hospital=self.request.user.hospital
        ).select_related(
            'patient' 
        ).order_by('-created_at')

class AIFollowupNotesViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def search_patients(self, request):
        try:
            name = request.query_params.get('name_patient', '')
            phone = request.query_params.get('patient_phone', '')
            
            # Build query based on provided parameters
            query = Q()
            if name:
                query |= Q(name_patient__icontains=name)
            if phone:
                query |= Q(patient_phone__icontains=phone)
            
            # Search patients belonging to this hospital
            patients = Patient.objects.filter(
                query,
                hospital=request.user.hospital
            ).values(
                'id_system',  # Changed from id to id_system
                'name_patient',
                'patient_phone',
                'date_of_birth'
            )[:10]  # Limit to 10 results

            # Add print for debugging
            print(f"Search query: {query}")
            print(f"Found patients: {patients}")
            
            # Format the results
            results = [{
                'id_system': patient['id_system'],  # No need to convert to string
                'name_patient': patient['name_patient'],
                'patient_phone': patient['patient_phone'],
                'display_text': f"{patient['name_patient']} ({patient['date_of_birth'].strftime('%Y-%m-%d')})"
            } for patient in patients]
            
            return Response({
                'results': results
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def create_notetaking(self, request):
        try:
            # Get patient by UUID (changed from ID)
            patient_id = request.data.get('patient_id_system') 
            if not patient_id:
                return Response(
                    {'error': 'Patient ID is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            patient = Patient.objects.get(
                id_system=patient_id, 
                hospital=request.user.hospital
            )
            
            # Create new notetaking record
            notetaking = FollowupNotetaking.objects.create(
                patient=patient,
                hospital=request.user.hospital
            )
            
            return Response({
                'message': 'Notetaking record created successfully',
                'notetaking_id': notetaking.id,
                'patient_name': patient.name_patient,
                'patient_phone': patient.patient_phone,
                'patient_id_system': patient.id_system  #  Regular ID
            })
            
        except Patient.DoesNotExist:
            return Response(
                {'error': 'Patient not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def save_raw(self, request, pk=None):
        try:
            notetaking = FollowupNotetaking.objects.get(
                id=pk,
                hospital=request.user.hospital  # Ensure the note belongs to this hospital
            )
            notetaking.raw_notes = request.data.get('raw_notes')
            notetaking.save()
            
            return Response({
                'message': 'Raw notes saved successfully',
                'raw_notes': notetaking.raw_notes,
                'notetaking_id': notetaking.id,
                'patient_name': notetaking.patient.name_patient
            })
        except FollowupNotetaking.DoesNotExist:
            return Response(
                {'error': 'Notetaking not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        try:
            notetaking = FollowupNotetaking.objects.get(
                id=pk,
                hospital=request.user.hospital
            )
            
            if not notetaking.raw_notes:
                return Response(
                    {'error': 'No raw notes found to process'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            service = BaiduAIService()
            success, processed_result = service.process_followup_notes_without_save(notetaking)
            
            if success:
                return Response({
                    'message': 'Notes processed successfully',
                    'raw_notes': notetaking.raw_notes,
                    'processed_notes': processed_result,
                    'notetaking_id': notetaking.id,
                    'patient_name': notetaking.patient.name_patient
                })
            
            return Response(
                {'error': str(processed_result)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
                
        except FollowupNotetaking.DoesNotExist:
            return Response(
                {'error': 'Notetaking not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def save_processed(self, request, pk=None):
        try:
            notetaking = FollowupNotetaking.objects.get(
                id=pk,
                hospital=request.user.hospital
            )
            processed_notes = request.data.get('processed_notes')
            
            if not processed_notes:
                return Response(
                    {'error': 'No processed notes provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            notetaking.processed_notes = processed_notes
            notetaking.save()
            
            return Response({
                'message': 'Processed notes saved successfully',
                'processed_notes': notetaking.processed_notes,
                'patient_name': notetaking.patient.name_patient
            })
            
        except FollowupNotetaking.DoesNotExist:
            return Response(
                {'error': 'Notetaking not found'},
                status=status.HTTP_404_NOT_FOUND
            )