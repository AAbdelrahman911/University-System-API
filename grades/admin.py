from django.contrib import admin
from .models import Grade

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'course', 'score', 'date_graded')
    list_filter = ('course', 'date_graded')
    search_fields = ('student__username', 'course__name')
    ordering = ('-date_graded',)



