import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')
django.setup()

from django.test import RequestFactory
from faculty.views import FacultyViewSet
from students.models import Student

factory = RequestFactory()
request = factory.get('/api/faculty/1/students/?department=1&year=2&date=2026-07-17&period=1')
# Mock user role to bypass permission
class MockUser:
    def getattr(self, attr, default=None): return default
    @property
    def role(self): return 'admin'
    @property
    def is_authenticated(self): return True

request.user = MockUser()

view = FacultyViewSet.as_view({'get': 'students'})
response = view(request, pk=1)
if hasattr(response, 'render'):
    response.render()

for student in response.data:
    print(student['name'], student.get('auto_status', 'None'))
