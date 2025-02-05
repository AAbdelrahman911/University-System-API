from django.db import models
from users.models import User
from courses.models import Course
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00')),
        MaxValueValidator(Decimal('100.00'))
    ])

    date_graded = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-date_graded']

    def get_grade_category(self):
        score = float(self.score)
        if score < 50:
            return 'Failed'
        elif 50 <= score < 65:
            return "Approved"
        elif 65 <= score < 80:
            return "Good"
        elif 80 <= score < 90:
            return "Very Good"
        elif 90 <= score <= 100:
            return "Excellent"
        else:
            return "Invalid Score"

    
    def __str__(self):
        return f"{self.student} - {self.course}: {self.score} "
