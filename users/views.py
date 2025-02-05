from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
from courses.models import Enrollment
from grades.models import Grade
from attendance.models import Attendance
from courses.serializers import EnrollmentSerializer
from grades.serializers import GradeSerializer
from attendance.serializers import AttendanceSerializer
from .serializers import ProfessrListSerializer,StudentOutputSerializer
from rest_framework import serializers
from courses.serializers import CourseOutputDashboardSerializer
from courses.models import Course
from courses.serializers import EnrollmentOutputDashboardSerializer
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



    permission_classes = [permissions.AllowAny]
    throttle_scope = 'anon'

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = 'user'

    def get_object(self):
        return self.request.user
    
class ProfessorListView(generics.ListAPIView):
    queryset = User.objects.filter(user_type = 'professor')
    serializer_class = ProfessrListSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = 'user'



class StudentDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = 'user'
    def get(self, request):
        if request.user.user_type != 'student':
            raise serializers.ValidationError("You are not a student!")
        student = request.user
        enrollments = Enrollment.objects.filter(student = student)
        grades = Grade.objects.filter(student = student)
        attendance = Attendance.objects.filter(student = student)
        grade_categories = [grade.get_grade_category() for grade in grades] 


        data = {
            'enrollments': EnrollmentOutputDashboardSerializer(enrollments, many = True).data,
            'grades': GradeSerializer(grades, many = True).data,
            'attendance': AttendanceSerializer(attendance, many = True).data,
            'grade_categories': grade_categories
        }

        return Response(data)
    

class ProfessorDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = 'user'
    def get(self, request):
        if request.user.user_type != 'professor':
            raise serializers.ValidationError("You are not a professor!")
        professor = request.user
        courses = Course.objects.filter(professor = professor)
        students = User.objects.filter(courses__professor = professor).distinct()
        data = {
            'courses': CourseOutputDashboardSerializer(courses, many = True).data,
            'students': StudentOutputSerializer(students, many = True).data
        }
        return Response(data)



        


