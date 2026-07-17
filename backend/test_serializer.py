import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')
django.setup()

from students.models import Student
from students.serializers import StudentSerializer

students = Student.objects.filter(department_id=1, year=2)
serializer = StudentSerializer(students, many=True)
data = serializer.data

for d in data:
    d['auto_status'] = 'leave'
    
print(data[0])
