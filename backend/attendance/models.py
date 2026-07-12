from django.db import models
from students.models import Student, Subject
from faculty.models import Faculty

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('leave', 'Leave (LV)'),
        ('on_duty', 'On Duty (OD)'),
    )
    
    attendance_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    period_number = models.IntegerField(default=1)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    marked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'date', 'period_number')
        
    def __str__(self):
        return f"{self.student.roll_number} - {self.date} P{self.period_number} - {self.status}"

class PeriodTiming(models.Model):
    period_number = models.IntegerField(primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['period_number']
        
    def __str__(self):
        return f"Period {self.period_number} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"
