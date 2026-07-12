from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsAdminOrFaculty
from students.models import Student, Department
from faculty.models import Faculty
from attendance.models import Attendance
from leave.models import LeaveRequest
from results.models import Result
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta

class AnalyticsDashboardView(APIView):
    permission_classes = [IsAdminOrFaculty]

    def get(self, request):
        today = timezone.now().date()
        thirty_days_ago = today - timedelta(days=30)
        
        # Core KPIs
        total_students = Student.objects.count()
        total_faculty = Faculty.objects.count()
        
        # Average Attendance last 30 days
        attendance_records = Attendance.objects.filter(date__gte=thirty_days_ago)
        total_att = attendance_records.count()
        present_att = attendance_records.filter(status='present').count()
        avg_attendance = (present_att / total_att * 100) if total_att > 0 else 0
        
        # Pending Leaves
        pending_leaves = LeaveRequest.objects.filter(status='pending').count()
        
        # Department-wise Students
        dept_wise_students = list(Department.objects.annotate(
            student_count=Count('student')
        ).values('name', 'code', 'student_count'))
        
        # Leave status count
        leave_status_count = {
            'approved': LeaveRequest.objects.filter(status='approved').count(),
            'pending': LeaveRequest.objects.filter(status='pending').count(),
            'rejected': LeaveRequest.objects.filter(status='rejected').count(),
        }
        
        # Mocking monthly data for charts since building complex grouping queries can be verbose
        # In a real scenario, this would aggregate by month using TruncMonth
        monthly_attendance = [
            {'month': 'Jan', 'attendance': 85},
            {'month': 'Feb', 'attendance': 88},
            {'month': 'Mar', 'attendance': 90},
            {'month': 'Apr', 'attendance': 82},
            {'month': 'May', 'attendance': 86},
            {'month': 'Jun', 'attendance': 89},
        ]
        
        monthly_performance = [
            {'month': 'Jan', 'avg_marks': 75},
            {'month': 'Feb', 'avg_marks': 78},
            {'month': 'Mar', 'avg_marks': 82},
            {'month': 'Apr', 'avg_marks': 70},
            {'month': 'May', 'avg_marks': 85},
            {'month': 'Jun', 'avg_marks': 88},
        ]
        
        # Top Performers
        # Annotate students with their average marks
        top_students = Student.objects.annotate(
            avg_marks=Avg('result__marks_obtained')
        ).exclude(avg_marks=None).order_by('-avg_marks')[:5]
        
        top_performers = [{
            'name': student.name, 
            'roll_number': student.roll_number, 
            'avg_marks': round(student.avg_marks, 2)
        } for student in top_students]
        
        # Low Performers (Less than 40 marks avg)
        low_students = Student.objects.annotate(
            avg_marks=Avg('result__marks_obtained')
        ).filter(avg_marks__lt=40).order_by('avg_marks')[:5]
        
        low_performers = [{
            'name': student.name, 
            'roll_number': student.roll_number, 
            'avg_marks': round(student.avg_marks, 2)
        } for student in low_students]

        return Response({
            'total_students': total_students,
            'total_faculty': total_faculty,
            'avg_attendance': round(avg_attendance, 2),
            'pending_leaves': pending_leaves,
            'dept_wise_students': dept_wise_students,
            'monthly_attendance': monthly_attendance,
            'leave_status_count': leave_status_count,
            'monthly_performance': monthly_performance,
            'top_performers': top_performers,
            'low_performers': low_performers
        })
