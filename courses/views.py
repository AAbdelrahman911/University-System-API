from rest_framework import viewsets, permissions, status, serializers, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from users.models import User
from users.serializers import StudentOutputSerializer
from django_filters.rest_framework import DjangoFilterBackend

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = 'user'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['professor']

    def get_queryset(self):
        if self.request.user.user_type == 'professor':
            return Course.objects.filter(professor = self.request.user)

        return Course.objects.all()
    
    def perform_create(self, serializer):
        if self.request.user.user_type != 'professor':
            raise serializers.ValidationError({'detail': 'Only Professors can create Courses!'},
                            status=status.HTTP_403_FORBIDDEN)
        serializer.save(professor = self.request.user)
    
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        course = self.get_object()
        students = course.students.all()
        raise serializers.ValidationError(
            {'course': course.name,
             'students': [s.get_full_name() for s in students]}
        )   
    
    
    @action(detail=False, methods=['get'])
    def prof_students(self, request):
        if request.user.user_type != 'professor':
            raise serializers.ValidationError("You are not a professor!")
        professor = request.user
        students = User.objects.filter(courses__professor=professor).distinct()
        serializer = StudentOutputSerializer(students, many=True)
        return Response(serializer.data)



class EnrollmentViewSet(viewsets.ModelViewSet):

    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = 'user'

    def get_queryset(self):
        return Enrollment.objects.filter(student = self.request.user)
    
    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        student = self.request.user

        if student.enrollment_count >= 7:
            raise serializers.ValidationError(
                {"detail": "Maximum course limit (7) reached"},
                code=status.HTTP_400_BAD_REQUEST
            )
        
        if student.enrollments.filter(course = course).exists():
            raise serializers.ValidationError(
                {"detail": "Already enrolled in this course"},
                code=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(student = student)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.student != request.user:
            raise serializers.ValidationError("You can only drop your own enrollments!")
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=False, methods=['get'])
    def my_enrollments(self,request):
        if request.user.user_type != 'student':
            raise serializers.ValidationError("You are not a student!")
        enrollments = self.get_queryset().filter(student = request.user)
        serializer = self.get_serializer(enrollments, many = True)
        return Response(serializer.data)

    

