import os
import django
from django.test import RequestFactory

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')
django.setup()

from faculty.views import FacultyViewSet
from faculty.models import Faculty

factory = RequestFactory()
request = factory.get('/api/faculty/1/students/', {'date': '2026-07-17', 'period': '1'})
# need to simulate user?
faculty = Faculty.objects.first()
# Actually let's just use the viewset method
view = FacultyViewSet.as_view({'get': 'students'})
response = view(request, pk=faculty.faculty_id)
print(response.data)
