import os
import sys
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "campus_management.settings")
sys.path.append(r"c:\Users\preet\OneDrive\Desktop\Campus_Management\backend")
django.setup()

from authentication.models import User
from faculty.models import Faculty
from students.models import Timetable
from authentication.serializers import UserSerializer

try:
    user = User.objects.get(name__icontains='nila')
    print("User:", user.email, user.role)
    
    faculty = Faculty.objects.filter(user=user).first()
    if faculty:
        print("Faculty found:", faculty.faculty_id, faculty.name)
    else:
        print("NO FACULTY PROFILE LINKED TO NILA!")

    serializer = UserSerializer(user)
    print("Serializer data:")
    print(serializer.data)

except Exception as e:
    print("Error:", e)
