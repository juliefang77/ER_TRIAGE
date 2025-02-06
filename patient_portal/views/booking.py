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
from django_filters.rest_framework import DjangoFilterBackend

from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from django_filters import FilterSet  # Add this import
from django_filters import FilterSet, CharFilter, ChoiceFilter  # Import specific filters

# Import patient-specific authentication
from .auth import PatientTokenAuthentication

# 患者小filter
class PatientBookingFilter(FilterSet):
    class Meta:
        model = BookingOnline
        fields = ['status']  # Fields that can be filtered


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


from rest_framework.pagination import PageNumberPagination

# 患者看已下单的 bookings pagination
class PatientBookingPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# 患者下单 book appointment and make payment
class BookingViewSet(viewsets.ModelViewSet):
    queryset = BookingOnline.objects.all()
    serializer_class = BookingCreateSerializer
    authentication_classes = [PatientTokenAuthentication]
    filter_backends = [DjangoFilterBackend] 
    filterset_class = PatientBookingFilter  # Filter by status
    pagination_class = PatientBookingPagination

    def get_queryset(self):
        return BookingOnline.objects.filter(
            patient_user=self.request.user
        ).select_related('hospital')  # Add this for performance
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming bookings (PATIENT_SUBMITTED or HOSPITAL_ACCEPTED)"""
        queryset = self.get_queryset().filter(
            status__in=['PATIENT_SUBMITTED', 'HOSPITAL_ACCEPTED']
        ).order_by('start_time')  # Order by appointment time

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def historical(self, request):
        """Get historical bookings (CONSULTATION_COMPLETED or CANCELLED)"""
        queryset = self.get_queryset().filter(
            status__in=['CONSULTATION_COMPLETED', 'CANCELLED']
        ).order_by('-actual_time')  # Order by completion time, most recent first

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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

class HospitalBookingPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class HospitalBookingFilter(FilterSet):
    actual_time_start = CharFilter(field_name='actual_time', lookup_expr='gte')
    actual_time_end = CharFilter(field_name='actual_time', lookup_expr='lte')
    patient_name = filters.CharFilter(field_name='patient_user__first_name', lookup_expr='icontains')
    patient_phone = filters.CharFilter(field_name='patient_user__phone', lookup_expr='icontains')
    status = filters.ChoiceFilter(choices=BookingOnline.APPOINTMENT_STATUS)

    class Meta:
        model = BookingOnline
        fields = ['actual_time_start', 'actual_time_end', 'patient_name', 'patient_phone', 'status']


# 医院管理订单
class HospitalBookingViewSet(viewsets.ModelViewSet):
    serializer_class = HospitalBookingSerializer
    pagination_class = HospitalBookingPagination
    filterset_class = HospitalBookingFilter
    search_fields = ['patient_user__first_name', 'patient_user__phone']
    
    def get_queryset(self):
        return BookingOnline.objects.filter(
            hospital=self.request.user.hospital
        ).select_related('patient_user').order_by('-start_time')
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get all pending bookings (PATIENT_SUBMITTED)"""
        queryset = self.get_queryset().filter(status='PATIENT_SUBMITTED')
        return self.get_paginated_response(
            self.get_serializer(self.paginate_queryset(queryset), many=True).data
        )
    
    @action(detail=False, methods=['get'])
    def accepted(self, request):
        """Get all accepted bookings (HOSPITAL_ACCEPTED)"""
        queryset = self.get_queryset().filter(status='HOSPITAL_ACCEPTED')
        return self.get_paginated_response(
            self.get_serializer(self.paginate_queryset(queryset), many=True).data
        )
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get completed and cancelled bookings"""
        queryset = self.get_queryset().filter(
            status__in=['CONSULTATION_COMPLETED', 'CANCELLED']
        )
        filtered_queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get booking statistics"""
        queryset = self.get_queryset()
        return Response({
            'pending_count': queryset.filter(status='PATIENT_SUBMITTED').count(),
            'accepted_count': queryset.filter(status='HOSPITAL_ACCEPTED').count(),
            'completed_count': queryset.filter(status='CONSULTATION_COMPLETED').count(),
            'cancelled_count': queryset.filter(status='CANCELLED').count(),
        })
    
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
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a booking with reason"""
        booking = self.get_object()
        
        # Check if booking can be rejected
        if booking.status != 'PATIENT_SUBMITTED':
            return Response(
                {'error': '只能拒绝待处理的预约'}, 
                status=400
            )
            
        # Get and validate reject reason
        reject_reason = request.data.get('reject_reason')
        if not reject_reason:
            return Response(
                {'error': '请提供拒绝原因'}, 
                status=400
            )
            
        # Update booking status and reason
        booking.status = 'CANCELLED'
        booking.reject_reason = reject_reason
        booking.save()
        
        serializer = self.get_serializer(booking)
        return Response(serializer.data)