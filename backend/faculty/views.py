from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Faculty
from .serializers import FacultySerializer, FacultyCreateUpdateSerializer
from authentication.permissions import IsAdmin, IsOwnerOrAdmin, IsAdminOrFaculty
from students.models import Student
from students.serializers import StudentSerializer

class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department__code', 'designation']
    search_fields = ['name', 'employee_id', 'email']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FacultyCreateUpdateSerializer
        return FacultySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        elif self.action in ['list']:
            permission_classes = [IsAdminOrFaculty]
        else:
            permission_classes = [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        faculty = self.get_object()
        dept_id = request.query_params.get('department')
        if dept_id:
            students = Student.objects.filter(department_id=dept_id)
        elif faculty.department:
            students = Student.objects.filter(department=faculty.department)
        else:
            return Response([])
            
        year = request.query_params.get('year')
        section = request.query_params.get('section')
        
        if year:
            students = students.filter(year=year)
        if section:
            students = students.filter(section=section)
            
        serializer = StudentSerializer(students, many=True)
        data = [dict(item) for item in serializer.data]
        
        date_str = request.query_params.get('date')
        period_str = request.query_params.get('period')
        
        if date_str:
            from leave.models import LeaveRequest, FacultyODAssignment
            
            # Find approved leaves for this date
            leaves = LeaveRequest.objects.filter(
                status='approved',
                from_date__lte=date_str,
                to_date__gte=date_str,
                student__in=students
            )
            
            # Find ODs for this date
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
                    if not period_str or (not od.from_period) or (od.from_period <= int(period_str) <= od.to_period):
                        is_od = True
                        break
                        
                if is_od:
                    student_data['auto_status'] = 'on_duty'
                    continue
                    
                # Check for Leave
                is_leave = False
                student_leaves = leaves.filter(student_id=student_id)
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
                    
        return Response(data)

    @action(detail=True, methods=['get'])
    def today_classes(self, request, pk=None):
        from django.utils import timezone
        faculty = self.get_object()
        today = timezone.localtime(timezone.now()).strftime('%A')
        from students.models import Timetable
        from students.serializers import TimetableSerializer
        
        classes = Timetable.objects.filter(faculty=faculty, day_of_week=today).order_by('period_number')
        serializer = TimetableSerializer(classes, many=True)
        return Response(serializer.data)
