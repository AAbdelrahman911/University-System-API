from rest_framework import serializers
from .models import Attendance
from users.models import User

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name']

class AttendanceSerializer(serializers.ModelSerializer):
    weekly_attendance_percentage = serializers.FloatField(read_only=True)
    student = StudentSerializer(read_only=True)
    class Meta:
        model = Attendance
        fields = '__all__'

    def validate(self, data):
        if not data['student'].courses.filter(id=data['course'].id).exists():
             raise serializers.ValidationError("Student is not enrolled in this course")
        return data
