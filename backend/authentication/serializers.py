from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(source='date_joined', read_only=True)
    student_id = serializers.SerializerMethodField()
    faculty_id = serializers.SerializerMethodField()
    designation = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'role', 'is_active', 'created_at', 'student_id', 'faculty_id', 'designation')
        read_only_fields = ('id', 'created_at')

    def get_student_id(self, obj):
        if hasattr(obj, 'student_profile') and obj.student_profile:
            return obj.student_profile.student_id
        return None

    def get_faculty_id(self, obj):
        if hasattr(obj, 'faculty_profile') and obj.faculty_profile:
            return obj.faculty_profile.faculty_id
        return None

    def get_designation(self, obj):
        if hasattr(obj, 'faculty_profile') and obj.faculty_profile:
            return obj.faculty_profile.designation
        return None

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            # Resolve email from Faculty or Student profiles if direct User not found
            resolved_email = email
            from authentication.models import User
            if not User.objects.filter(email=email).exists():
                from faculty.models import Faculty
                from students.models import Student
                
                faculty_profile = Faculty.objects.filter(email=email).first()
                if faculty_profile and faculty_profile.user:
                    resolved_email = faculty_profile.user.email
                else:
                    student_profile = Student.objects.filter(email=email).first()
                    if student_profile and student_profile.user:
                        resolved_email = student_profile.user.email

            user = authenticate(request=self.context.get('request'), email=resolved_email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password.")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")
            
        data['user'] = user
        return data
