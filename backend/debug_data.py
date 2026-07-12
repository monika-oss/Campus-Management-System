import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')
django.setup()

from faculty.models import Faculty
from students.models import Student, Timetable

print('--- Staff Rekha ---')
try:
    rekha = Faculty.objects.get(name__icontains='rekha')
    dept_code = rekha.department.code if rekha.department else 'None'
    print(f'Name: {rekha.name}, Dept: {dept_code}, ID: {rekha.faculty_id}')
    tts = Timetable.objects.filter(faculty=rekha)
    print(f'Classes Assigned: {tts.count()}')
    for t in tts:
        print(f'  - {t.day_of_week} P{t.period_number}: Dept={t.department.code}, Yr={t.year}, Sec={t.section}')
except Exception as e:
    print('Error finding Rekha:', e)

print('\n--- Student Ram ---')
try:
    ram = Student.objects.get(name__icontains='ram')
    dept_code = ram.department.code if ram.department else 'None'
    print(f'Name: {ram.name}, Dept: {dept_code}, Yr: {ram.year}, Sec: {ram.section}')
except Exception as e:
    print('Error finding Ram:', e)
