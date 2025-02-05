from django.contrib import admin
from .models import Attendance
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'present')
    list_filter = ('course', 'date', 'present')
    search_fields = ('student__username', 'course__name')
    ordering = ('-date',)    