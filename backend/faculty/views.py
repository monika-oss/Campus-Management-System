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
            
            leaves = LeaveRequest.objects.filter(
                from_date__lte=date_str,
                to_date__gte=date_str,
                student__in=students
            )
            
            ods = FacultyODAssignment.objects.filter(date=date_str).prefetch_related('students')
            
            for student_data in data:
                student_id = student_data['student_id']
                
                is_od = False
                for od in ods:
                    if any(s.student_id == student_id for s in od.students.all()):
                        # Default bounds if one is missing but the other exists
                        fp = od.from_period
                        tp = od.to_period
                        
                        if fp and not tp:
                            tp = fp
                        elif tp and not fp:
                            fp = tp
                            
                        if fp and tp and period_str:
                            if fp <= int(period_str) <= tp:
                                is_od = True
                                break
                        elif not fp and not tp:
                            # Full day OD
                            is_od = True
                            break
                            
                if is_od:
                    student_data['auto_status'] = 'on_duty'
                    continue
                    
                student_leaves = leaves.filter(student_id=student_id)
                student_data['leave_status'] = None
                student_data['leave_pending'] = False

                # ── PASS 1: Period-wise leave (highest priority after OD) ──────────
                # Check if this specific period has an approved/pending period-wise leave.
                # This must run BEFORE the full-day check so that a student who has
                # a pending full-day leave + an approved period-wise leave correctly
                # shows L (not A) for the approved periods.
                period_leave_found = False
                if period_str:
                    for leave in student_leaves:
                        if not leave.is_partial_day:
                            continue  # skip full-day leaves in this pass
                        if not (leave.from_period and leave.to_period):
                            continue
                        if leave.from_period <= int(period_str) <= leave.to_period:
                            if leave.status == 'rejected':
                                continue # Ignore rejected leaves, keep looking
                                
                            period_leave_found = True
                            if leave.status == 'approved':
                                # Period-wise approved → L (Leave) pre-selected
                                student_data['auto_status'] = 'leave'
                                student_data['leave_status'] = 'approved'
                            elif leave.status in ('pending_advisor', 'pending_hod'):
                                # Period-wise pending → A default + badge
                                student_data['leave_pending'] = True
                                student_data['leave_status'] = leave.status
                            break  # one active period-wise leave per student per period

                # ── PASS 2: Full-day leave (only if no period-wise leave found) ────
                # Full day leave → A in attendance regardless of approval.
                # Approval is administrative; faculty manually marks attendance.
                if not period_leave_found:
                    for leave in student_leaves:
                        if leave.is_partial_day:
                            continue  # skip period-wise leaves in this pass
                        if leave.status == 'approved':
                            student_data['leave_status'] = 'approved'
                            # intentionally NO auto_status = 'leave' for full-day
                            break
                        elif leave.status in ('pending_advisor', 'pending_hod'):
                            student_data['leave_pending'] = True
                            student_data['leave_status'] = leave.status
                            break
                            
        return Response(data)

    @action(detail=False, methods=['get'], permission_classes=[], authentication_classes=[])
    def debug_leaves(self, request):
        from leave.models import LeaveRequest
        leaves = LeaveRequest.objects.all().values('leave_id', 'student_id', 'status', 'from_date', 'to_date', 'is_partial_day', 'from_period', 'to_period')
        return Response(list(leaves))

    @action(detail=False, methods=['get'], permission_classes=[], authentication_classes=[])
    def debug_ods(self, request):
        from leave.models import FacultyODAssignment
        ods = list(FacultyODAssignment.objects.all().values('assignment_id', 'date', 'from_period', 'to_period', 'reason'))
        for od in ods:
            obj = FacultyODAssignment.objects.get(assignment_id=od['assignment_id'])
            od['students'] = list(obj.students.values_list('student_id', flat=True))
        return Response(ods)
        
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
