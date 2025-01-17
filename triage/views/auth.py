# Authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from triage.serializers.triage_serializer import HospitalLoginSerializer

#Authentication for hospitals
class CustomAuthToken(ObtainAuthToken):
    serializer_class = HospitalLoginSerializer  # Specify the serializer class
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'hospital': user.hospital.id if user.hospital else None
        })
