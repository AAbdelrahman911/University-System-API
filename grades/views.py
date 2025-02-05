from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from .models import Grade
from .serializers import GradeSerializer
from users.models import User


class GradeViewSet(viewsets.ModelViewSet):
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = 'user'
    filterset_fields = ['course', 'score']
    search_fields = ['course__name', 'student__username']
    
    def get_queryset(self):
        if self.request.user.user_type == 'professor':
             return Grade.objects.filter(course__professor=self.request.user)
        return Grade.objects.filter(student=self.request.user)
    
    def perform_create(self, serializer):
        if self.request.user.user_type != 'professor':
            raise serializers.ValidationError(
                {'detail': 'Only professors can sumbit grades'},
                status= status.HTTP_403_FORBIDDEN
            )
        serializer.save()

    @action(detail=False, methods=['get'])
    def my_grades(self, request):
        if request.user.user_type != 'student':
            raise serializers.ValidationError("You are not a student!")
        grades = Grade.objects.filter(student = request.user)
        serializer = self.get_serializer(grades, many = True)
        return Response(serializer.data)

