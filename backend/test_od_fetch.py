import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')
django.setup()

from students.models import Student
from leave.models import FacultyODAssignment

date_str = '2026-07-17'
student = Student.objects.filter(roll_number='REG2026EEE003').first()
if student:
    student_id = student.student_id
    ods = FacultyODAssignment.objects.filter(date=date_str)
    print("Total ODs on date:", ods.count())

    student_ods = ods.filter(students__student_id=student_id)
    print("ODs for student:", student_ods.count())

    for od in student_ods:
        print(f"OD ID: {od.id}, From: {od.from_period}, To: {od.to_period}")
else:
    print("Student not found")
