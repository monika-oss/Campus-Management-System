from django.db import models
from authentication.models import User
from students.models import Department

class Faculty(models.Model):
    faculty_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile', null=True, blank=True)
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    DESIGNATION_CHOICES = (
        ('Assistant Professor', 'Assistant Professor'),
        ('Associate Professor', 'Associate Professor'),
        ('Professor', 'Professor'),
        ('HOD', 'Head of Department'),
    )
    designation = models.CharField(max_length=100, choices=DESIGNATION_CHOICES, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    qualification = models.CharField(max_length=100, blank=True, null=True)
    experience_years = models.IntegerField(blank=True, null=True)
    profile_photo = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        import datetime
        year_str = str(datetime.datetime.now().year)
        dept_code = self.department.code if self.department else "GEN"
        expected_prefix = f"EMP{year_str}{dept_code}"
        
        if not self.employee_id or not self.employee_id.startswith(expected_prefix):
            latest_faculty = Faculty.objects.filter(employee_id__startswith=expected_prefix).order_by('-employee_id').first()
            if latest_faculty:
                try:
                    seq_str = latest_faculty.employee_id[len(expected_prefix):]
                    seq = int(seq_str) + 1
                except ValueError:
                    seq = 1
            else:
                seq = 1
            self.employee_id = f"{expected_prefix}{seq:03d}"

        if not self.user:
            from authentication.models import User
            user_exists = User.objects.filter(email=self.email).first()
            if user_exists:
                self.user = user_exists
            else:
                new_user = User.objects.create_user(
                    email=self.email,
                    password='faculty123',
                    name=self.name,
                    role='faculty'
                )
                self.user = new_user
        else:
            # Sync existing user
            if self.user.email != self.email or self.user.name != self.name:
                self.user.email = self.email
                self.user.name = self.name
                self.user.save()

        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        user_to_delete = self.user
        super().delete(*args, **kwargs)
        if user_to_delete:
            user_to_delete.delete()

    def __str__(self):
        return f"{self.employee_id} - {self.name}"
