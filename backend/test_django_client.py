import os
import django
from django.test.client import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')
django.setup()

from rest_framework.test import APIClient
from authentication.models import User
user = User.objects.first()
client = APIClient()
client.force_authenticate(user=user)

response = client.get('/api/faculty/1/students/?date=2026-07-17&period=1&department=3')
print("Status:", response.status_code)
print("Students returned:", len(response.json()))
for s in response.json():
    print(s.get('roll_number'), s.get('auto_status'))
