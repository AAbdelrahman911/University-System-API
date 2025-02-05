from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Enrollment

@receiver(post_save, sender=Enrollment)
def increment_enrollment_count(sender, instance, created, **kwargs):
    if created:
        instance.student.enrollment_count += 1
        instance.student.save()

@receiver(post_delete, sender=Enrollment)
def decrement_enrollment_count(sender, instance, **kwargs):
    instance.student.enrollment_count -= 1
    instance.student.save()
