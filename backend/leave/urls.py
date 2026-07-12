from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaveRequestViewSet, FacultyODAssignmentViewSet

router = DefaultRouter()
router.register(r'od', FacultyODAssignmentViewSet, basename='od')
router.register(r'', LeaveRequestViewSet, basename='leave')

urlpatterns = [
    path('', include(router.urls)),
]
