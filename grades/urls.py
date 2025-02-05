from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import GradeViewSet

router = DefaultRouter()
router.register(r'grades', GradeViewSet, basename='grade')

urlpatterns = [
    path('my-grades/', GradeViewSet.as_view({'get': 'my_grades'}), name='my-grades'),
] + router.urls