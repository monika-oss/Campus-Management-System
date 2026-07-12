from django.db import models
from students.models import Student
from faculty.models import Faculty

class LeaveRequest(models.Model):
    TYPE_CHOICES = (
        ('medical', 'Medical'),
        ('personal', 'Personal'),
        ('academic', 'Academic'),
        ('emergency', 'Emergency'),
        ('other', 'Other'),
    )
    
    STATUS_CHOICES = (
        ('pending_advisor', 'Pending Advisor Approval'),
        ('pending_hod', 'Pending HOD Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    leave_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    from_date = models.DateField()
    to_date = models.DateField()
    is_partial_day = models.BooleanField(default=False)
    from_period = models.IntegerField(null=True, blank=True)
    to_period = models.IntegerField(null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_advisor')
    advisor_reviewer = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True, related_name='advisor_reviewed_leaves')
    advisor_reviewed_at = models.DateTimeField(null=True, blank=True)
    advisor_remarks = models.TextField(blank=True, null=True)
    
    hod_reviewer = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True, related_name='hod_reviewed_leaves')
    hod_reviewed_at = models.DateTimeField(null=True, blank=True)
    hod_remarks = models.TextField(blank=True, null=True)
    
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.roll_number} - {self.leave_type} ({self.status})"

class FacultyODAssignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    assigned_by = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='assigned_ods')
    students = models.ManyToManyField(Student, related_name='assigned_ods')
    date = models.DateField()
    from_period = models.IntegerField(null=True, blank=True)
    to_period = models.IntegerField(null=True, blank=True)
    reason = models.TextField()
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OD by {self.assigned_by.name} on {self.date}"
