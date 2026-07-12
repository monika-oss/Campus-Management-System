from rest_framework import serializers
from .models import Faculty
from students.serializers import DepartmentSerializer
from students.models import Timetable

class FacultySerializer(serializers.ModelSerializer):
    department_details = DepartmentSerializer(source='department', read_only=True)
    subjects_taught = serializers.SerializerMethodField()
    
    class Meta:
        model = Faculty
        fields = '__all__'

    def get_subjects_taught(self, obj):
        timetables = Timetable.objects.filter(faculty=obj).select_related('subject')
        subjects = set(t.subject.subject_name for t in timetables if t.subject)
        return list(subjects)

class FacultyCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'
