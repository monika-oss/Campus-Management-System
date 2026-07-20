from rest_framework import serializers
from .models import Student, Department, Subject

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    department_details = DepartmentSerializer(source='department', read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'

class StudentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    department_details = DepartmentSerializer(source='department', read_only=True)
    
    class Meta:
        model = Subject
        fields = '__all__'

class TimetableSerializer(serializers.ModelSerializer):
    subject_details = SubjectSerializer(source='subject', read_only=True)
    timetable_department_details = DepartmentSerializer(source='department', read_only=True)
    # Cannot easily nest FacultySerializer without circular import, so just provide IDs or simple dict
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)
    
    class Meta:
        model = __import__('students.models', fromlist=['Timetable']).Timetable
        fields = '__all__'
