# patient_portal/authentication.py
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class PatientTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = self.get_model().objects.get(key=key)
            if not token.user.phone:  # Make sure it's a patient user
                raise AuthenticationFailed('Not a patient user')
            return (token.user, token)
        except self.get_model().DoesNotExist:
            raise AuthenticationFailed('Invalid token')