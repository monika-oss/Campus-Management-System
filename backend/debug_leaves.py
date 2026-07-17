import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')
django.setup()

from leave.models import LeaveRequest
from students.models import Student

leaves = LeaveRequest.objects.all()
print("All leaves:")
for l in leaves:
    print(f"ID: {l.leave_id}, Student: {l.student.name}, From: {l.from_date}, To: {l.to_date}, Status: {l.status}, Partial: {l.is_partial_day}, From P: {l.from_period}, To P: {l.to_period}")
