from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import LeaveRequest, FacultyODAssignment
from .serializers import LeaveRequestSerializer, LeaveRequestCreateSerializer, LeaveRequestUpdateSerializer, FacultyODAssignmentSerializer
from authentication.permissions import IsAdminOrFaculty, IsOwnerOrAdmin

class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all().order_by('-applied_at')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'leave_type', 'student__department']
    search_fields = ['student__name', 'student__roll_number', 'reason']

    def get_serializer_class(self):
        if self.action == 'create':
            return LeaveRequestCreateSerializer
        elif self.action in ['update', 'partial_update', 'approve', 'reject']:
            return LeaveRequestUpdateSerializer
        return LeaveRequestSerializer

    def get_permissions(self):
        if self.action in ['approve', 'reject']:
            permission_classes = [IsAdminOrFaculty]
        else:
            permission_classes = [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        student = self.request.user.student_profile if hasattr(self.request.user, 'student_profile') else None
        serializer.save(student=student)

    @action(detail=True, methods=['put'])
    def approve(self, request, pk=None):
        leave = self.get_object()
        faculty = request.user.faculty_profile if hasattr(request.user, 'faculty_profile') else None
        
        if not faculty:
            return Response({'error': 'Only faculty can approve leaves.'}, status=status.HTTP_403_FORBIDDEN)
            
        remarks = request.data.get('remarks', '')
        
        from notifications.models import Notification
        
        if leave.status == 'pending_advisor':
            leave.status = 'pending_hod'
            leave.advisor_reviewer = faculty
            leave.advisor_reviewed_at = timezone.now()
            leave.advisor_remarks = remarks
        elif leave.status == 'pending_hod':
            if faculty.designation != 'HOD':
                return Response({'error': 'Only the HOD can give the final approval.'}, status=status.HTTP_403_FORBIDDEN)
            if faculty.department != leave.student.department:
                return Response({'error': 'You can only approve leaves for students in your own department.'}, status=status.HTTP_403_FORBIDDEN)
                
            leave.status = 'approved'
            leave.hod_reviewer = faculty
            leave.hod_reviewed_at = timezone.now()
            leave.hod_remarks = remarks
        else:
            return Response({'error': 'Leave request is not in a state that can be approved.'}, status=status.HTTP_400_BAD_REQUEST)
            
        leave.save()
        
        if leave.status == 'approved':
            # Notify Student only on final approval
            Notification.objects.create(
                title='Leave Request Approved',
                description=f'Your leave request was approved by the HOD.',
                target_role='student',
                target_user=leave.student.user,
                notification_type='success',
                related_module='leave'
            )
        
        serializer = LeaveRequestSerializer(leave)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def reject(self, request, pk=None):
        leave = self.get_object()
        faculty = request.user.faculty_profile if hasattr(request.user, 'faculty_profile') else None
        remarks = request.data.get('remarks', '')
        
        from notifications.models import Notification
        
        if leave.status == 'pending_advisor':
            leave.advisor_reviewer = faculty
            leave.advisor_reviewed_at = timezone.now()
            leave.advisor_remarks = remarks
            level = 'Class Advisor'
        else:
            leave.hod_reviewer = faculty
            leave.hod_reviewed_at = timezone.now()
            leave.hod_remarks = remarks
            level = 'HOD'
            
        leave.status = 'rejected'
        leave.save()
        
        # Notify Student
        Notification.objects.create(
            title='Leave Request Rejected',
            description=f'Your leave request was rejected by {level}.',
            target_role='student',
            target_user=leave.student.user,
            notification_type='error',
            related_module='leave'
        )
        
        serializer = LeaveRequestSerializer(leave)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='student/(?P<student_id>[^/.]+)')
    def student_leaves(self, request, student_id=None):
        leaves = LeaveRequest.objects.filter(student_id=student_id).order_by('-applied_at')
        serializer = self.get_serializer(leaves, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def approved_on_date(self, request):
        date_str = request.query_params.get('date')
        period_str = request.query_params.get('period_number')
        
        if not date_str:
            return Response([])
            
        queryset = LeaveRequest.objects.filter(
            status='approved',
            from_date__lte=date_str,
            to_date__gte=date_str
        )
        
        if period_str:
            try:
                period = int(period_str)
                queryset = queryset.exclude(
                    is_partial_day=True,
                    from_period__gt=period
                ).exclude(
                    is_partial_day=True,
                    to_period__lt=period
                )
            except ValueError:
                pass
                
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my(self, request):
        if not hasattr(request.user, 'student_profile'):
            return Response({'error': 'Only students can view their leaves.'}, status=status.HTTP_403_FORBIDDEN)
        leaves = LeaveRequest.objects.filter(student=request.user.student_profile).order_by('-applied_at')
        serializer = self.get_serializer(leaves, many=True)
        return Response(serializer.data)


class FacultyODAssignmentViewSet(viewsets.ModelViewSet):
    queryset = FacultyODAssignment.objects.all().order_by('-assigned_at')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['assigned_by', 'date']
    search_fields = ['students__name', 'students__roll_number', 'reason']

    def get_serializer_class(self):
        return FacultyODAssignmentSerializer

    def get_permissions(self):
        permission_classes = [IsAdminOrFaculty]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        pass

    def create(self, request, *args, **kwargs):
        faculty = request.user.faculty_profile if hasattr(request.user, 'faculty_profile') else None
        
        # Get roll numbers array from request
        roll_numbers = request.data.get('students', [])
        if isinstance(roll_numbers, str):
            roll_numbers = [r.strip() for r in roll_numbers.split(',') if r.strip()]
            
        from students.models import Student
        students = Student.objects.filter(roll_number__in=roll_numbers)
        
        if not students.exists():
            return Response({'error': 'No valid students found for the given roll numbers.'}, status=status.HTTP_400_BAD_REQUEST)

        # Remove 'students' from request data if it's there so the serializer doesn't complain about invalid PKs
        data = request.data.copy()
        if 'students' in data:
            del data['students']

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        od_assignment = serializer.save(assigned_by=faculty)
        
        # Assign the found students
        od_assignment.students.set(students)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)