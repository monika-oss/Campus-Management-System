import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_campus.settings')
django.setup()

from authentication.models import User
from students.models import Department, Student
from faculty.models import Faculty

print("--- Seeding Database ---")

# 1. Create Department
cse, created = Department.objects.get_or_create(code="CSE", defaults={"name": "Computer Science & Engineering"})
print(f"Department CSE: {'Created' if created else 'Already exists'}")

ece, created = Department.objects.get_or_create(code="ECE", defaults={"name": "Electronics & Communication Engineering"})
print(f"Department ECE: {'Created' if created else 'Already exists'}")

# 2. Create Admin User
admin_email = "admin@example.com"
admin_user = User.objects.filter(email=admin_email).first()
if not admin_user:
    admin_user = User.objects.create_superuser(
        email=admin_email,
        password="admin123",
        name="Administrator",
        role="admin"
    )
    print(f"Admin User created: {admin_email} / admin123")
else:
    print(f"Admin User already exists: {admin_email}")

# 3. Create Faculty Member
faculty_email = "nila@example.com"
faculty_name = "Nila"
faculty_user = User.objects.filter(email=faculty_email).first()
if not faculty_user:
    faculty_user = User.objects.create_user(
        email=faculty_email,
        password="faculty123",
        name=faculty_name,
        role="faculty"
    )
faculty, created = Faculty.objects.get_or_create(
    email=faculty_email,
    defaults={
        "name": faculty_name,
        "department": cse,
        "designation": "HOD",
        "user": faculty_user
    }
)
print(f"Faculty Member Nila: {'Created' if created else 'Already exists'} (Login: nila@example.com / faculty123)")

# 4. Create Student
student_email = "ram@example.com"
student_name = "Ram"
student_user = User.objects.filter(email=student_email).first()
if not student_user:
    student_user = User.objects.create_user(
        email=student_email,
        password="student123",
        name=student_name,
        role="student"
    )
student, created = Student.objects.get_or_create(
    email=student_email,
    defaults={
        "name": student_name,
        "department": cse,
        "year": 3,
        "section": "A",
        "user": student_user
    }
)
print(f"Student Ram: {'Created' if created else 'Already exists'} (Login: ram@example.com / student123)")

print("Database Seeding Completed!")
