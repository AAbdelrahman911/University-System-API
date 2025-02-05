from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student','Student'),
        ('professor','Professor'),
    )
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES)
    student_id = models.CharField(max_length=20, unique= True, null= True, blank= True)
    email= models.EmailField(unique= True)
    enrollment_count = models.PositiveIntegerField(default=0, editable= False)
    def __str__(self):
        return f'{self.get_full_name()} ({self.user_type})'
    
    