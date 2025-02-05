from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Attendance
from .serializers import AttendanceSerializer
from rest_framework import serializers

class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    throttle_scope = 'user'

    def get_queryset(self):
        if self.request.user.user_type == 'professor':
            return Attendance.objects.filter(course__professor = self.request.user)
        return Attendance.objects.filter(student = self.request.user)
    
    def perform_create(self, serializer):
        if self.request.user.user_type != 'professor':
            raise serializers.ValidationError(
                {"detail": "Only professors can mark attendance"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()