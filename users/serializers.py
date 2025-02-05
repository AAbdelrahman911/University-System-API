from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    enrollment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['username','email','password','first_name','enrollment_count','last_name','user_type','student_id']
        extra_kwargs = {
            'password': {'write_only': True},
            }
   

    def create(self,validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            user_type=validated_data['user_type'],
            student_id=validated_data['student_id'],
            )
        return user
    
class ProfessrListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','first_name','last_name']

class StudentOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','first_name','last_name','student_id']






