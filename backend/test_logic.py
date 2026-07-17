import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')
django.setup()

from students.models import Student
from students.serializers import StudentSerializer
from leave.models import LeaveRequest

students = Student.objects.filter(name__icontains='yogeshwaran')
print("Students:", students)
date_str = '2026-07-17'
period_str = '1'

leaves = LeaveRequest.objects.filter(
    status='approved',
    from_date__lte=date_str,
    to_date__gte=date_str,
    student__in=students
)

print("Leaves:", leaves)

data = [dict(item) for item in StudentSerializer(students, many=True).data]

for student_data in data:
    student_id = student_data['student_id']
    print(f"Checking student_id: {student_id}")
    
    is_leave = False
    student_leaves = leaves.filter(student_id=student_id)
    print(f"Student Leaves: {student_leaves}")
    
    for leave in student_leaves:
        if not leave.is_partial_day:
            is_leave = True
            break
        elif period_str and leave.from_period and leave.to_period:
            if leave.from_period <= int(period_str) <= leave.to_period:
                is_leave = True
                break
                
    if is_leave:
        student_data['auto_status'] = 'leave'

for d in data:
    print(d['name'], d.get('auto_status', 'None'))
