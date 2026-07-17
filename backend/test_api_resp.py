import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')
django.setup()

from students.models import Student
from students.serializers import StudentSerializer
from django.test import RequestFactory
from faculty.views import FacultyViewSet

factory = RequestFactory()
request = factory.get('/api/faculty/1/students/?department=1&year=2&date=2026-07-17&period=1')
view = FacultyViewSet.as_view({'get': 'students'})
response = view(request, pk=1)
print(response.data[0] if response.data else "Empty")
