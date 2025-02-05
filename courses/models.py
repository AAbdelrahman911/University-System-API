from django.db import models
from users.models import User
from django.core.exceptions import ValidationError

class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=15, unique=True)
    professor = models.ForeignKey(User, on_delete= models.CASCADE, limit_choices_to={'user_type':'professor'})
    students = models.ManyToManyField(User, related_name='courses',limit_choices_to={'user_type':'student'})

    def __str__(self):
        return f'{self.code} - {self.name}'
    
class Enrollment(models.Model):
        student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
        course = models.ForeignKey(Course, on_delete= models.CASCADE)
        data_enrolled = models.DateTimeField(auto_now_add=True)

        class Meta:
            unique_together = ['student', 'course']

        def clean(self):
            if self.student.enrollments.count() >= 7:
                  raise ValidationError("Maximum of 7 courses allowed per student")

            if Enrollment.objects.filter(student = self.student, course = self.course).exists():
                 raise ValidationError("Student is already enrolled in this course")

        def save(self, *args, **kwargs):
            self.full_clean()
            super().save(*args,**kwargs)
        
        def __str__(self):
            return f"{self.student.first_name} {self.student.last_name} - {self.course.name}"
