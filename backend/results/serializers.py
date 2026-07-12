from rest_framework import serializers
from .models import Result
from students.serializers import StudentSerializer, SubjectSerializer
from faculty.serializers import FacultySerializer

class ResultSerializer(serializers.ModelSerializer):
    student_details = StudentSerializer(source='student', read_only=True)
    subject_details = SubjectSerializer(source='subject', read_only=True)
    entered_by_details = FacultySerializer(source='entered_by', read_only=True)
    
    class Meta:
        model = Result
        fields = '__all__'

class ResultCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'
