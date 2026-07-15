import os
import django
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import User
from students.models import Department, Student, Subject, Timetable
from faculty.models import Faculty
import datetime

class APISystemTests(APITestCase):
    def setUp(self):
        # Setup basic data
        self.dept = Department.objects.create(code="CSE", name="Computer Science")
        
        self.admin_user = User.objects.create_superuser(
            email="admin_test@test.com", password="adminpassword", name="Admin", role="admin"
        )
        
        self.faculty_user = User.objects.create_user(
            email="faculty_test@test.com", password="facultypassword", name="Faculty User", role="faculty"
        )
        self.faculty = Faculty.objects.create(
            name="Faculty User", department=self.dept, email="faculty_test@test.com", user=self.faculty_user
        )
        
        self.student_user = User.objects.create_user(
            email="student_test@test.com", password="studentpassword", name="Student User", role="student"
        )
        self.student = Student.objects.create(
            name="Student User", department=self.dept, year=1, section="A", email="student_test@test.com", user=self.student_user
        )
        
        self.subject = Subject.objects.create(
            subject_name="Test Subject", subject_code="SUB101", department=self.dept, year=1
        )

    def test_authentication_login(self):
        url = '/api/auth/login/'
        response = self.client.post(url, {'email': 'admin_test@test.com', 'password': 'adminpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        
        # Test invalid credentials
        response = self.client.post(url, {'email': 'admin_test@test.com', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_faculty_crud_as_admin(self):
        url = '/api/faculty/'
        self.client.force_authenticate(user=self.admin_user)
        
        # Test list
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test create
        data = {
            'name': 'New Faculty',
            'department': self.dept.id,
            'email': 'new_faculty@test.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='new_faculty@test.com').exists())
        
        faculty_id = response.data['faculty_id']
        
        # Test delete
        detail_url = f'{url}{faculty_id}/'
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify orphaned user bug fix! User should be deleted.
        self.assertFalse(User.objects.filter(email='new_faculty@test.com').exists())

    def test_student_crud_as_admin(self):
        url = '/api/students/'
        self.client.force_authenticate(user=self.admin_user)
        
        # Create student
        data = {
            'name': 'New Student',
            'department': self.dept.id,
            'year': 2,
            'section': 'B',
            'email': 'new_student@test.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        student_id = response.data['student_id']
        detail_url = f'{url}{student_id}/'
        
        # Delete student
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(email='new_student@test.com').exists())

    def test_timetable_assignment(self):
        url = '/api/students/timetable/'
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            'department': self.dept.id,
            'year': 1,
            'section': 'A',
            'day_of_week': 'Monday',
            'period_number': 1,
            'start_time': '09:00',
            'end_time': '09:50',
            'subject': self.subject.subject_id,
            'faculty': self.faculty.faculty_id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
