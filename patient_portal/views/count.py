'''
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from django.db.models import Count
from django.db import models
from ..models import PatientTriageSubmission


class HospitalFillingCountViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """Get counts only for the logged-in hospital"""
        hospital = request.user.hospital
        counts = PatientTriageSubmission.objects.filter(
            hospital=hospital
        ).aggregate(
            filling_count=Count('id', filter=models.Q(status='FILLING')),
            fillout_count=Count('id', filter=models.Q(status='PENDING'))
        )
        return Response({
            'hospital_id': hospital.id,
            **counts
        })

    def retrieve(self, request, pk=None):
        """Ensure hospital can only see their own counts"""
        if str(request.user.hospital.id) != str(pk):
            return Response(
                {'error': 'Not authorized to view this hospital\'s data'}, 
                status=403
            )
            
        filling_count = PatientTriageSubmission.objects.filter(
            hospital=request.user.hospital,
            status='FILLING'
        ).count()
        
        fillout_count = PatientTriageSubmission.objects.filter(
            hospital=request.user.hospital,
            status='PENDING'
        ).count()
        
        return Response({
            'hospital_id': pk,
            'filling_count': filling_count,
            'fillout_count': fillout_count
        })'''