from rest_framework import serializers
from .models import Course, Enrollment
from users.models import User
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course

        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ['date_enrolled']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name']

class CourseOutputDashboardSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ['id','name','code', 'students']

class CourseSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name','code']


class EnrollmentOutputDashboardSerializer(serializers.ModelSerializer):
    course = CourseSerializer2(read_only=True)
    class Meta:
        model = Enrollment
        fields = ['course','data_enrolled']
