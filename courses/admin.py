from django.contrib import admin
from .models import Course, Enrollment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'professor')
    list_filter = ('name', 'professor')
    search_fields = ('professor__username', 'code', 'name')
    ordering = ('professor',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'course', 'data_enrolled')
    list_filter = ('course',)
    search_fields = ('course__name', 'student__username')
    ordering = ('-data_enrolled',)
