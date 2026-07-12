import os
import sys
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_campus.settings")
sys.path.append(r"c:\Users\preet\OneDrive\Desktop\Campus_Management\backend")
django.setup()

from rest_framework.test import APIRequestFactory, force_authenticate
from faculty.views import FacultyViewSet
from faculty.models import Faculty
from authentication.models import User

factory = APIRequestFactory()
user = User.objects.filter(role='faculty').first()

request = factory.get('/api/faculty/1/today_classes/')
force_authenticate(request, user=user)

view = FacultyViewSet.as_view({'get': 'today_classes'})
try:
    response = view(request, pk=1)
    print(response.status_code)
    print(response.data)
except Exception as e:
    import traceback
    traceback.print_exc()
