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
            return Response(serializer.data)
        return Response([])

    @action(detail=True, methods=['get'])
    def today_classes(self, request, pk=None):
        import datetime
        faculty = self.get_object()
        today = datetime.datetime.now().strftime('%A')
        from students.models import Timetable
        from students.serializers import TimetableSerializer
        
        classes = Timetable.objects.filter(faculty=faculty, day_of_week=today).order_by('period_number')
        serializer = TimetableSerializer(classes, many=True)
        return Response(serializer.data)
