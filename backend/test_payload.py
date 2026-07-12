import os, django, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')
django.setup()
from django.test import RequestFactory
from rest_framework.test import force_authenticate
from authentication.models import User
from attendance.views import AttendanceViewSet

rekha_user = User.objects.get(email__icontains='rekha')

json_data = '{"subject_id": "5", "date": "2026-07-05", "period_number": "2", "attendances": [{"student_id": "4", "status": "present"}]}'

factory = RequestFactory()
request = factory.post('/api/attendance/mark/', json_data, content_type='application/json')
force_authenticate(request, user=rekha_user)

view = AttendanceViewSet.as_view({'post': 'mark'})
try:
    response = view(request)
    print(response.status_code, response.data)
except Exception as e:
    import traceback
    traceback.print_exc()
