from patient_portal.serializers.booking_serializer import BookingCreateSerializer, HospitalBookingSerializer
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
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.authentication import SessionAuthentication

from rest_framework import authentication
from rest_framework import exceptions
from patient_portal.models import PatientUser
# filters
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

# 患者小filter
class PatientBookingFilter(FilterSet):
    class Meta:
        model = BookingOnline
        fields = ['status']  # Fields that can be filtered

# 患者app的自定义authentication
class PatientPhoneAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Skip this auth method for hospital endpoints
        if not request.path.startswith('/apipatient/'):
            return None
            
        phone = request.META.get('HTTP_X_PATIENT_PHONE')
        password = request.META.get('HTTP_X_PATIENT_PASSWORD')
        
        if not phone or not password:
            return None

        try:
            patient = PatientUser.objects.get(phone=phone)
            if patient.check_password(password):
                return (patient, None)
        except PatientUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such patient')

        return None

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

# 患者下单 book appointment and make payment
class BookingViewSet(viewsets.ModelViewSet):
    queryset = BookingOnline.objects.all()
    serializer_class = BookingCreateSerializer
    authentication_classes = [PatientPhoneAuthentication]
    filter_backends = [DjangoFilterBackend] 
    filterset_class = PatientBookingFilter  # Filter by status

    def get_queryset(self):
        return BookingOnline.objects.filter(
            patient_user=self.request.user
        ).select_related('hospital')  # Add this for performance

    def create(self, request, *args, **kwargs):
        """Create initial booking when patient selects time slot and hospital"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save booking with patient_user
        booking = serializer.save(
            patient_user=request.user,  # Use request.user directly
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

# 医院管理订单
class HospitalBookingViewSet(viewsets.ModelViewSet):
    serializer_class = HospitalBookingSerializer
    # No need to specify authentication_classes since we're using default TokenAuthentication
    
    def get_queryset(self):
        return BookingOnline.objects.filter(
            hospital=self.request.user.hospital
        ).select_related('patient_user').order_by('-start_time')  # Fix parenthesis
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accept a booking and optionally modify time"""
        booking = self.get_object()
        
        # Check if booking can be accepted
        if booking.status != 'PATIENT_SUBMITTED':
            return Response(
                {'error': '只能接受待处理的预约'}, 
                status=400
            )
            
        # Update time slots if provided
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        if start_time and end_time:
            booking.start_time = start_time
            booking.end_time = end_time
            
        # Accept the booking
        booking.status = 'HOSPITAL_ACCEPTED'
        booking.save()
        
        serializer = self.get_serializer(booking)
        return Response(serializer.data)
        
    def update(self, request, *args, **kwargs):
        """Allow updating time slots for accepted bookings"""
        booking = self.get_object()
        
        # Only allow time modifications for accepted bookings
        if booking.status not in ['PATIENT_SUBMITTED', 'HOSPITAL_ACCEPTED']:
            return Response(
                {'error': '只能修改待处理或已接受的预约时间'}, 
                status=400
            )
            
        return super().update(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark a booking as completed after consultation"""
        booking = self.get_object()
        
        # Check if booking can be completed
        if booking.status != 'HOSPITAL_ACCEPTED':
            return Response(
                {'error': '只能完成已接受的预约'}, 
                status=400
            )
            
        # Mark as completed
        booking.status = 'CONSULTATION_COMPLETED'
        booking.save()
        
        serializer = self.get_serializer(booking)
        return Response(serializer.data)