from rest_framework import serializers
from .models import LeaveRequest, FacultyODAssignment
from students.serializers import StudentSerializer
from faculty.serializers import FacultySerializer

class LeaveRequestSerializer(serializers.ModelSerializer):
    student_details = StudentSerializer(source='student', read_only=True)
    reviewed_by_details = FacultySerializer(source='reviewed_by', read_only=True)
    
    class Meta:
        model = LeaveRequest
        fields = '__all__'

class LeaveRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ('leave_id', 'leave_type', 'from_date', 'to_date', 'reason', 'is_partial_day', 'from_period', 'to_period', 'status', 'student')
        read_only_fields = ('leave_id', 'status', 'student')
        
class LeaveRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ('status', 'reviewed_by', 'reviewed_at')

class FacultyODAssignmentSerializer(serializers.ModelSerializer):
    assigned_by_details = FacultySerializer(source='assigned_by', read_only=True)
    students_details = StudentSerializer(source='students', many=True, read_only=True)
    
    class Meta:
        model = FacultyODAssignment
        fields = '__all__'
