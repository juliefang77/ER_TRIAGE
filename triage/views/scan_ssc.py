from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from ..services.scan_ssc import SocialSecurityReader
from rest_framework.permissions import AllowAny

class SocialSecurityViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    """
    ViewSet for social security card reading operations
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.card_service = SocialSecurityReader(
            api_key=settings.ID_BAIDU_KEY,
            secret_key=settings.ID_BAIDU_SECRET
        )

    @action(detail=False, methods=['POST'])
    def read_card(self, request):
        """
        Read and extract information from social security card image
        
        Expected request data:
        {
            "image": "base64_encoded_image_string"
        }
        """
        try:
            base64_image = request.data.get('image')
            
            if not base64_image:
                return Response(
                    {'error': 'No image provided'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            result = self.card_service.process_card(base64_image)
            
            if not result['success']:
                return Response(
                    {'error': result['error']}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )