from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, DepartmentViewSet, TimetableViewSet, SubjectViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'timetable', TimetableViewSet, basename='timetable')
router.register(r'', StudentViewSet, basename='student')

urlpatterns = [
    path('', include(router.urls)),
]
