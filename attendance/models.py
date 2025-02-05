from django.db import models
from users.models import User
from courses.models import Course


class Attendance(models.Model):
    student= models.ForeignKey(User, on_delete= models.CASCADE)
    course = models.ForeignKey(Course, on_delete= models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default= False)
    
    class Meta:
        unique_together = ['student', 'course', 'date']
        ordering = ['-date']


    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.course.name} - {self.date}"

