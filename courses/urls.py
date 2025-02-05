from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register(r'courses',CourseViewSet,basename='course')
router.register(r'enrollments',EnrollmentViewSet,basename='enrollment')

urlpatterns = [
    path('available/',CourseViewSet.as_view({'get': 'list'}), name='course-list'),
    path('my_enrollments/',EnrollmentViewSet.as_view({'get': 'my_enrollments'}), name='my_enrollments'),
    path('professor/students/',CourseViewSet.as_view({'get': 'prof_students'}), name='prof_students'),    
] + router.urls