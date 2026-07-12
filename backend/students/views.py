from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Student, Department
from .serializers import StudentSerializer, StudentCreateUpdateSerializer, DepartmentSerializer
from authentication.permissions import IsAdmin, IsAdminOrFaculty, IsOwnerOrAdmin

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department', 'department__code', 'year', 'section']
    search_fields = ['name', 'roll_number', 'email']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return StudentCreateUpdateSerializer
        return StudentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        elif self.action in ['list']:
            permission_classes = [IsAdminOrFaculty]
        else:
            permission_classes = [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        student = self.get_object()
        attendances = student.attendance_set.all().order_by('-date')
        from attendance.serializers import AttendanceSerializer
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)
    @action(detail=True, methods=['get'])
    def attendance_summary(self, request, pk=None):
        student = self.get_object()
        attendances = student.attendance_set.all()
        
        total_classes = attendances.count()
        total_present = attendances.filter(status='present').count()
        total_absent = attendances.filter(status='absent').count()
        total_leave = attendances.filter(status='leave').count()
        overall_percentage = (total_present / total_classes * 100) if total_classes > 0 else 0

        from collections import defaultdict
        subject_data = defaultdict(lambda: {'total': 0, 'present': 0})
        
        for att in attendances:
            subj_name = att.subject.subject_name
            subject_data[subj_name]['total'] += 1
            if att.status == 'present':
                subject_data[subj_name]['present'] += 1
                
        subjects_list = []
        for subj_name, data in subject_data.items():
            pct = (data['present'] / data['total'] * 100) if data['total'] > 0 else 0
            subjects_list.append({
                'subject_name': subj_name,
                'total': data['total'],
                'present': data['present'],
                'percentage': pct
            })

        return Response({
            'overall_percentage': overall_percentage,
            'total_present': total_present,
            'total_absent': total_absent,
            'total_leave': total_leave,
            'subjects': subjects_list
        })

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        student = self.get_object()
        results = student.result_set.filter(is_published=True).order_by('-semester')
        from results.serializers import ResultSerializer
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)

from .models import Subject
from .serializers import SubjectSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

from .models import Timetable
from .serializers import TimetableSerializer

class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['department', 'department__code', 'year', 'section', 'day_of_week', 'faculty']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
