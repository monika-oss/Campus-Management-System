import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')
django.setup()

from django.test import RequestFactory
from faculty.views import FacultyViewSet

factory = RequestFactory()
request = factory.get('/api/faculty/1/students/', {'date': '2026-07-17', 'period': '1'})
# We need to test the logic directly to avoid auth issues
from faculty.models import Faculty
from students.models import Student
from students.serializers import StudentSerializer
from leave.models import LeaveRequest, FacultyODAssignment

students = Student.objects.all()
serializer = StudentSerializer(students, many=True)
data = [dict(item) for item in serializer.data]

date_str = '2026-07-17'
period_str = '1'

ods = FacultyODAssignment.objects.filter(
    date=date_str,
    students__in=students
)

for student_data in data:
    student_id = student_data['student_id']
    
    # Check for OD
    is_od = False
    student_ods = ods.filter(students__student_id=student_id)
    for od in student_ods:
        if od.from_period and od.to_period and period_str:
            if od.from_period <= int(period_str) <= od.to_period:
                is_od = True
                break
        elif not od.from_period and not od.to_period:
            is_od = True
            break
            
    if is_od:
        student_data['auto_status'] = 'on_duty'
        continue

for student in data:
    if student['roll_number'] == 'REG2026EEE003':
        print(f"Maha: {student.get('auto_status')}")
    if student['roll_number'] == 'REG2026EEE001':
        print(f"Yogesh: {student.get('auto_status')}")
