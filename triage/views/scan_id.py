from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.conf import settings
from ..services.scan_id import IDCardReader

class IDCardViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    """
    ViewSet for ID card reading operations
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_card_service = IDCardReader(
            api_key=settings.ID_BAIDU_KEY,
            secret_key=settings.ID_BAIDU_SECRET
        )

    @action(detail=False, methods=['POST'])
    def read_card(self, request):
        """
        Read and extract information from ID card image
        
        Expected request data:
        {
            "image": "base64_encoded_image_string"
        }
        """
        try:
            # Get base64 image from request
            base64_image = request.data.get('image')
            
            if not base64_image:
                return Response(
                    {'error': 'No image provided'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Process the ID card
            result = self.id_card_service.process_id_card(base64_image)
            
            if not result['success']:
                return Response(
                    {'error': result['error']}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Return the flattened response
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )