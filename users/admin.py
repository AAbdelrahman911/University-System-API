from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'user_type', 'student_id')
    list_filter = ('user_type',)
    search_fields = ('username', 'email', 'first_name', 'last_name', 'student_id')
