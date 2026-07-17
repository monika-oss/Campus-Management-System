import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')
django.setup()

from attendance.models import Attendance
atts = Attendance.objects.filter(date='2026-07-17', period_number=1)
for a in atts:
    print(a.student.name, a.status)
