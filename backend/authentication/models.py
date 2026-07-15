from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        # Superuser must have admin role
        if extra_fields.get('role') != 'admin':
            extra_fields['role'] = 'admin'

        return self.create_user(email, password, **extra_fields)
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
    )
    
    # Override username to use email instead
    username = None
    email = models.EmailField(_('email address'), unique=True)
    
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'role']
    
    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if not is_new:
            # Sync to Faculty profile if exists
            if hasattr(self, 'faculty_profile') and self.faculty_profile:
                profile = self.faculty_profile
                if profile.email != self.email or profile.name != self.name:
                    profile.email = self.email
                    profile.name = self.name
                    from faculty.models import Faculty
                    super(Faculty, profile).save()
            # Sync to Student profile if exists
            if hasattr(self, 'student_profile') and self.student_profile:
                profile = self.student_profile
                if profile.email != self.email or profile.name != self.name:
                    profile.email = self.email
                    profile.name = self.name
                    from students.models import Student
                    super(Student, profile).save()
