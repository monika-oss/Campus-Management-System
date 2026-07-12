from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from .models import Attendance
from .serializers import AttendanceSerializer, AttendanceCreateUpdateSerializer, BulkAttendanceSerializer
from authentication.permissions import IsAdminOrFaculty, IsOwnerOrAdmin
from students.models import Student
from faculty.models import Faculty

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all().order_by('-date', 'student__roll_number')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['date', 'student__department', 'student__section', 'subject', 'period_number']
    search_fields = ['student__name', 'student__roll_number']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AttendanceCreateUpdateSerializer
        return AttendanceSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'mark']:
            permission_classes = [IsAdminOrFaculty]
        else:
            permission_classes = [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def mark(self, request):
        serializer = BulkAttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        subject_id = serializer.validated_data['subject_id']
        date = serializer.validated_data['date']
        period_number = serializer.validated_data.get('period_number', 1)
        attendances = serializer.validated_data['attendances']
        
        faculty = None
        if hasattr(request.user, 'faculty_profile'):
            faculty = request.user.faculty_profile

        created_count = 0
        updated_count = 0

        for att in attendances:
            student_id = att.get('student_id')
            status_val = att.get('status')
            
            obj, created = Attendance.objects.update_or_create(
                student_id=student_id,
                date=date,
                period_number=period_number,
                defaults={'status': status_val, 'faculty': faculty, 'subject_id': subject_id}
            )
            if created:
                created_count += 1
            else:
                updated_count += 1
                
        return Response({
            'message': f'Attendance marked successfully. Created: {created_count}, Updated: {updated_count}'
        }, status=status.HTTP_200_OK)



    def get_period_status(self, current_time_str, todays_classes):
        import datetime
        current_time = datetime.datetime.strptime(current_time_str, '%H:%M').time()
        
        active_period = None
        past_periods = []
        
        for tt in todays_classes:
            if tt.start_time <= current_time <= tt.end_time:
                active_period = tt
            elif current_time > tt.end_time:
                past_periods.append(tt)
                
        return active_period, past_periods


    @action(detail=False, methods=['get'])
    def current_status(self, request):
        if not hasattr(request.user, 'student_profile'):
            return Response({'detail': 'Only students can access this.'}, status=status.HTTP_403_FORBIDDEN)
            
        student = request.user.student_profile
        import datetime
        from django.utils import timezone
        from students.models import Timetable
        
        today = datetime.date.today()
        day_name = today.strftime("%A")
        
        # current_time_str = datetime.datetime.now().strftime("%H:%M") 
        # Hardcoding a time for testing if needed, or use actual
        current_time_str = datetime.datetime.now().strftime("%H:%M")
        
        # Get today's timetable for the student
        todays_classes = Timetable.objects.filter(
            department=student.department,
            year=student.year,
            section=student.section,
            day_of_week=day_name
        )
        
        active_period, past_periods = self.get_period_status(current_time_str, todays_classes)
        
        # Auto-absent logic for past periods
        for tt in past_periods:
            exists = Attendance.objects.filter(student=student, date=today, period_number=tt.period_number).exists()
            if not exists:
                Attendance.objects.create(
                    student=student,
                    date=today,
                    period_number=tt.period_number,
                    subject=tt.subject,
                    status='absent'
                )
        
        # Check active period
        if active_period:
            tt = active_period
            # Check if already marked
            exists = Attendance.objects.filter(student=student, date=today, period_number=tt.period_number).exists()
            if not exists:
                return Response({
                    'action': 'prompt',
                    'period': tt.period_number,
                    'subject_id': tt.subject.subject_id,
                    'subject_name': tt.subject.name,
                    'time_window': (tt.start_time.strftime('%H:%M'), tt.end_time.strftime('%H:%M'))
                }, status=status.HTTP_200_OK)
                    
        return Response({'action': 'none'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def check_in(self, request):
        if not hasattr(request.user, 'student_profile'):
            return Response({'detail': 'Only students can check in.'}, status=status.HTTP_403_FORBIDDEN)
            
        student = request.user.student_profile
        period_number = request.data.get('period_number')
        subject_id = request.data.get('subject_id')
        
        if not period_number or not subject_id:
            return Response({'detail': 'period_number and subject_id are required.'}, status=status.HTTP_400_BAD_REQUEST)
            
        import datetime
        from students.models import Subject
        
        today = datetime.date.today()
        try:
            subject = Subject.objects.get(pk=subject_id)
        except Subject.DoesNotExist:
            return Response({'detail': 'Invalid subject.'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Verify if they are trying to mark for the active period (Optional security check)
        current_time_str = datetime.datetime.now().strftime("%H:%M")
        day_name = today.strftime("%A")
        from students.models import Timetable
        todays_classes = Timetable.objects.filter(
            department=student.department,
            year=student.year,
            section=student.section,
            day_of_week=day_name
        )
        active_period, _ = self.get_period_status(current_time_str, todays_classes)
        
        if not active_period or str(active_period.period_number) != str(period_number):
            return Response({'detail': 'You can only check-in for the currently active period.'}, status=status.HTTP_400_BAD_REQUEST)
            
        obj, created = Attendance.objects.update_or_create(
            student=student,
            date=today,
            period_number=period_number,
            defaults={'status': 'present', 'subject': subject}
        )
        
        message = 'Checked in successfully.' if created else 'Already checked in for this period.'
        return Response({'message': message}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def report(self, request):
        department = request.query_params.get('department')
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        
        queryset = Student.objects.all()
        if department:
            queryset = queryset.filter(department_id=department)
            
        report_data = []
        for student in queryset:
            atts = Attendance.objects.filter(student=student)
            if month and year:
                atts = atts.filter(date__month=month, date__year=year)
                
            total = atts.count()
            present = atts.filter(status='present').count()
            percentage = (present / total * 100) if total > 0 else 0
            
            report_data.append({
                'student_id': student.student_id,
                'roll_number': student.roll_number,
                'name': student.name,
                'total_classes': total,
                'present': present,
                'percentage': round(percentage, 2)
            })
            
        return Response(report_data)

    @action(detail=False, methods=['get'], url_path='student/(?P<student_id>[^/.]+)')
    def student_attendance(self, request, student_id=None):
        attendances = Attendance.objects.filter(student_id=student_id).order_by('-date')
        serializer = self.get_serializer(attendances, many=True)
        return Response(serializer.data)


from rest_framework.permissions import IsAuthenticated
