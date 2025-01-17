from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from followup.models import FollowupNotetaking
from ..services.baidu_service import BaiduAIService

class AIFollowupNotesViewSet(viewsets.ViewSet):
    @action(detail=True, methods=['post'])
    def save_raw(self, request, pk=None):
        try:
            notetaking = FollowupNotetaking.objects.get(id=pk)
            notetaking.raw_notes = request.data.get('raw_notes')
            notetaking.save()
            
            return Response({
                'message': 'Raw notes saved successfully',
                'raw_notes': notetaking.raw_notes
            })
        except FollowupNotetaking.DoesNotExist:
            return Response(
                {'error': 'Notetaking not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        try:
            # Get the notetaking object
            notetaking = FollowupNotetaking.objects.get(id=pk)
            
            # Check if raw_notes exists
            if not notetaking.raw_notes:
                return Response(
                    {'error': 'No raw notes found to process'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Process with AI
            service = BaiduAIService()
            success, result = service.process_followup_notes(notetaking)
            
            if success:
                return Response({
                    'message': 'Notes processed successfully',
                    'raw_notes': notetaking.raw_notes,
                    'processed_notes': notetaking.processed_notes
                })
            
            return Response(
                {'error': str(result)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
                
        except FollowupNotetaking.DoesNotExist:
            return Response(
                {'error': 'Notetaking not found'},
                status=status.HTTP_404_NOT_FOUND
            )