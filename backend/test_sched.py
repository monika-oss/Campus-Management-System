import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')
django.setup()

from faculty.models import Timetable
schedules = Timetable.objects.filter(faculty_id=1)
for s in schedules:
    print(f"Subj: {s.subject}, Period: {s.period_number}, Dept: {s.department_id}, Year: {s.year}")
