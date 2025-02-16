from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from patient_portal.serializers.profile_serializer import PatientProfileSerializer, ChangePasswordSerializer, ForgetPasswordSerializer
from patient_portal.models.patient_user import PatientUser
from .auth import PatientTokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication

# 患者app查看、修改personal profile信息，更新密码
class PatientProfileViewSet(viewsets.GenericViewSet):
    serializer_class = PatientProfileSerializer
    authentication_classes = [PatientTokenAuthentication]
    
    def get_object(self):
        """
        Return the currently authenticated user's profile
        """
        return self.request.user
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get current user's profile
        """
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_me(self, request):
        """
        Update current user's profile
        """
        user = self.get_object()
        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True if request.method == 'PATCH' else False
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """
        Change user password
        """
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            user = self.get_object()
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': '密码修改成功'}, status=status.HTTP_200_OK)
    
    @action(
        detail=False, 
        methods=['post'], 
        permission_classes=[AllowAny],
        authentication_classes=[]
    )
    def forget_password(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = PatientUser.objects.get(
                phone=serializer.validated_data['phone'],
                first_name=serializer.validated_data['first_name']
            )
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({
                'message': '密码重置成功，请使用新密码登录'
            })