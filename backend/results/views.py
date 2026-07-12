from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Result
from .serializers import ResultSerializer, ResultCreateUpdateSerializer
from authentication.permissions import IsAdminOrFaculty, IsOwnerOrAdmin

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['student__department', 'academic_year', 'subject', 'semester', 'is_published']
    search_fields = ['student__name', 'student__roll_number']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ResultCreateUpdateSerializer
        return ResultSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'publish']:
            permission_classes = [IsAdminOrFaculty]
        else:
            permission_classes = [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        faculty = self.request.user.faculty_profile if hasattr(self.request.user, 'faculty_profile') else None
        serializer.save(entered_by=faculty)

    @action(detail=False, methods=['post'])
    def publish(self, request):
        semester = request.data.get('semester')
        subject_id = request.data.get('subject_id')
        
        results = Result.objects.filter(is_published=False)
        if semester:
            results = results.filter(semester=semester)
        if subject_id:
            results = results.filter(subject_id=subject_id)
            
        count = results.update(is_published=True)
        return Response({'message': f'{count} results published successfully.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='student/(?P<student_id>[^/.]+)')
    def student_results(self, request, student_id=None):
        results = Result.objects.filter(student_id=student_id, is_published=True).order_by('-semester')
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='subject/(?P<subject_id>[^/.]+)')
    def subject_results(self, request, subject_id=None):
        results = Result.objects.filter(subject_id=subject_id).order_by('-marks_obtained')
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)
