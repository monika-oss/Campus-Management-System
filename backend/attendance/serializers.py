from rest_framework import serializers
from .models import Attendance
from students.serializers import StudentSerializer, SubjectSerializer
from faculty.serializers import FacultySerializer

class AttendanceSerializer(serializers.ModelSerializer):
    student_details = StudentSerializer(source='student', read_only=True)
    faculty_details = FacultySerializer(source='faculty', read_only=True)
    subject_details = SubjectSerializer(source='subject', read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'

class AttendanceCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class BulkAttendanceSerializer(serializers.Serializer):
    subject_id = serializers.IntegerField()
    date = serializers.DateField()
    period_number = serializers.IntegerField(default=1)
    attendances = serializers.ListField(
        child=serializers.DictField()
    )

class PeriodTimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = __import__('attendance.models', fromlist=['PeriodTiming']).PeriodTiming
        fields = '__all__'
