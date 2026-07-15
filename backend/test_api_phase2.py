import os
import django
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import User
from students.models import Department, Student, Subject, Timetable
from faculty.models import Faculty
from attendance.models import Attendance
from results.models import Result
from leave.models import LeaveRequest
from notifications.models import Notification
import datetime

class APIPhase2Tests(APITestCase):
    def setUp(self):
        # Create department
        self.dept = Department.objects.create(code="CSE", name="Computer Science")
        
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            email="admin_test2@test.com", password="adminpassword", name="Admin", role="admin"
        )
        
        # Create standard faculty user & profile
        self.faculty_user = User.objects.create_user(
            email="faculty_test2@test.com", password="facultypassword", name="Faculty User", role="faculty"
        )
        self.faculty = Faculty.objects.create(
            name="Faculty User", department=self.dept, email="faculty_test2@test.com", user=self.faculty_user, designation="Assistant Professor"
        )

        # Create advisor user & profile
        self.advisor_user = User.objects.create_user(
            email="advisor_test@test.com", password="advisorpassword", name="Advisor User", role="faculty"
        )
        self.advisor = Faculty.objects.create(
            name="Advisor User", department=self.dept, email="advisor_test@test.com", user=self.advisor_user, designation="Associate Professor"
        )

        # Create HOD user & profile
        self.hod_user = User.objects.create_user(
            email="hod_test@test.com", password="hodpassword", name="HOD User", role="faculty"
        )
        self.hod = Faculty.objects.create(
            name="HOD User", department=self.dept, email="hod_test@test.com", user=self.hod_user, designation="HOD"
        )
        
        # Create student user & profile
        self.student_user = User.objects.create_user(
            email="student_test2@test.com", password="studentpassword", name="Student User", role="student"
        )
        self.student = Student.objects.create(
            name="Student User", department=self.dept, year=1, section="A", email="student_test2@test.com", user=self.student_user
        )
        
        # Create subject
        self.subject = Subject.objects.create(
            subject_name="Test Subject", subject_code="SUB101", department=self.dept, year=1
        )

    def test_attendance_mark_and_retrieve(self):
        url = '/api/attendance/'
        # Faculty marks bulk attendance
        self.client.force_authenticate(user=self.faculty_user)
        
        data = {
            'subject_id': self.subject.subject_id,
            'date': '2023-10-10',
            'period_number': 1,
            'attendances': [
                {'student_id': self.student.student_id, 'status': 'present'}
            ]
        }
        response = self.client.post(f'{url}mark/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Attendance marked successfully', response.data['message'])
        
        # Retrieve attendance as student
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'present')

    def test_leave_request_workflow(self):
        url = '/api/leave/'
        
        # Submit leave request as Student
        self.client.force_authenticate(user=self.student_user)
        leave_data = {
            'leave_type': 'medical',
            'from_date': '2023-10-11',
            'to_date': '2023-10-12',
            'reason': 'Sick',
            'is_partial_day': False
        }
        response = self.client.post(url, leave_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        leave_id = response.data['leave_id']
        self.assertEqual(response.data['status'], 'pending_advisor')
        
        # Approve as Advisor
        self.client.force_authenticate(user=self.advisor_user)
        response = self.client.put(f'{url}{leave_id}/approve/', {'remarks': 'Recommend'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'pending_hod')
        
        # Approve as HOD
        self.client.force_authenticate(user=self.hod_user)
        response = self.client.put(f'{url}{leave_id}/approve/', {'remarks': 'Fully Approved'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'approved')

    def test_results_publish_workflow(self):
        url = '/api/results/'
        self.client.force_authenticate(user=self.faculty_user)
        
        # Enter result (is_published = False)
        result_data = {
            'student': self.student.student_id,
            'subject': self.subject.subject_id,
            'marks_obtained': 85.00,
            'max_marks': 100.00,
            'grade': 'A',
            'semester': 1,
            'academic_year': '2023-2024',
            'is_published': False
        }
        response = self.client.post(url, result_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Publish result
        response = self.client.post(f'{url}publish/', {'semester': 1, 'subject_id': self.subject.subject_id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('published successfully', response.data['message'])
        
        # Retrieve result as Student
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(f'{url}student/{self.student.student_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(float(response.data[0]['marks_obtained']), 85.00)

    def test_analytics_dashboard(self):
        url = '/api/analytics/dashboard/'
        
        # Authenticated Admin retrieves dashboard
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_students', response.data)
        self.assertIn('total_faculty', response.data)
        
        # Authenticated Student gets forbidden
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_notifications_workflow(self):
        url = '/api/notifications/'
        
        # Admin creates warning notification
        self.client.force_authenticate(user=self.admin_user)
        notif_data = {
            'title': 'Test Warning',
            'description': 'This is a test warning',
            'notification_type': 'warning',
            'target_role': 'all',
            'is_active': True
        }
        response = self.client.post(url, notif_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        notif_id = response.data['notification_id']
        
        # Student views unread notification
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(f'{url}unread/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['notifications'][0]['title'], 'Test Warning')
        
        # Student marks notification as read
        response = self.client.post(f'{url}{notif_id}/read/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Student checks unread count again (should be 0)
        response = self.client.get(f'{url}unread/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
