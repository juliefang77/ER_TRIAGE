from patient_portal.serializers.booking_serializer import BookingCreateSerializer
from followup.models import BookingOnline
import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from patient_portal.services.booking import ShouqianbaService
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class PatientOnlyPermission(permissions.BasePermission):
    """Custom permission to only allow patients to access the view"""
    def has_permission(self, request, view):
        try:
            # Check if user has an associated PatientUser
            return hasattr(request.user, 'patientuser')
        except:
            return False

# Payment success webhook
@csrf_exempt
def payment_notify(request):
    data = json.loads(request.body)
    try:
        order_no = data.get('order_no', '')
        booking_id = order_no.split('_')[1]
        
        if data.get('status') == 'SUCCESS':
            booking = BookingOnline.objects.get(id=booking_id)
            booking.status = 'PATIENT_SUBMITTED'  # Confirm the status after payment
            booking.payment_id = data.get('trade_no')
            booking.save()
            
        return HttpResponse('success')
    except Exception as e:
        print(f"Payment notification error: {str(e)}")
        return HttpResponse('fail')

# 患者预约线上问诊并付费
class BookingViewSet(viewsets.ModelViewSet):
    queryset = BookingOnline.objects.all()
    serializer_class = BookingCreateSerializer
    permission_classes = [PatientOnlyPermission]  # Only allow patients
    authentication_classes = []  # Skip token authentication

    def create(self, request, *args, **kwargs):
        """Create initial booking when patient selects time slot and hospital"""
        # Get the patient_user from session
        if not hasattr(request.user, 'patientuser'):
            return Response(
                {'error': 'Please login as a patient'}, 
                status=403
            )
        """Create initial booking when patient selects time slot and hospital"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save booking with initial status and patient_user
        booking = serializer.save(
            patient_user=request.user.patientuser,
            status='PATIENT_SUBMITTED'
        )
        
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def create_payment(self, request, pk=None):
        """Create payment for an existing booking"""
        booking = self.get_object()
        payment_service = ShouqianbaService()
        
        # Get the QR code and payment info
        payment_info = payment_service.create_payment(booking)
        
        # Update booking with terminal trace
        booking.terminal_trace = payment_info['order_no']
        booking.save()
        
        return Response({
            'qr_code': payment_info['qr_code'],
            'order_no': payment_info['order_no']
        })