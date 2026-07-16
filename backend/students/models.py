from django.db import models
import datetime
from authentication.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    year = models.IntegerField()
    section = models.CharField(max_length=5, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_photo = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        import datetime
        year_str = str(datetime.datetime.now().year)
        dept_code = self.department.code if self.department else "GEN"
        expected_prefix = f"REG{year_str}{dept_code}"
        
        if not self.roll_number or not self.roll_number.startswith(expected_prefix):
            latest_student = Student.objects.filter(roll_number__startswith=expected_prefix).order_by('-roll_number').first()
            if latest_student:
                try:
                    seq_str = latest_student.roll_number[len(expected_prefix):]
                    seq = int(seq_str) + 1
                except ValueError:
                    seq = 1
            else:
                seq = 1
            self.roll_number = f"{expected_prefix}{seq:03d}"

        if not self.user:
            from authentication.models import User
            user_exists = User.objects.filter(email=self.email).first()
            if user_exists:
                self.user = user_exists
            else:
                new_user = User.objects.create_user(
                    email=self.email,
                    password='student123',
                    name=self.name,
                    role='student'
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
        return f"{self.roll_number} - {self.name}"

class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=150)
    subject_code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.IntegerField()
    credits = models.IntegerField(default=3)
    
    def __str__(self):
        return f"{self.subject_code} - {self.subject_name}"

class Timetable(models.Model):
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    )
    
    timetable_id = models.AutoField(primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.IntegerField()
    section = models.CharField(max_length=5, blank=True, null=True)
    day_of_week = models.CharField(max_length=15, choices=DAY_CHOICES)
    period_number = models.IntegerField()
    start_time = models.TimeField(default=datetime.time(9, 0))
    end_time = models.TimeField(default=datetime.time(9, 50))
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    faculty = models.ForeignKey('faculty.Faculty', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('department', 'year', 'section', 'day_of_week', 'period_number')
        
    def __str__(self):
        return f"{self.department.code} - Yr {self.year} Sec {self.section} - {self.day_of_week} P{self.period_number}"
