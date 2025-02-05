from django.urls import path
from .views import RegisterView, UserProfileView, ProfessorListView, StudentDashboardView, ProfessorDashboardView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', UserProfileView.as_view(), name='profile'),
    path('professors/', ProfessorListView.as_view(), name='professor-list'),
    path('student/dashboard/', StudentDashboardView.as_view(), name='student-dashboard'),
    path('professor/dashboard/', ProfessorDashboardView.as_view(), name='professor-dashboard'),
]