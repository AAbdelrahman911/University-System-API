from rest_framework import serializers
from .models import Grade

class GradeSerializer(serializers.ModelSerializer):
    grade_category = serializers.CharField(read_only=True, source='get_grade_category')    
    class Meta:
        model = Grade
        fields = ['student','course','score','grade_category','date_graded']
        read_only_fields = ['date_graded']
        

