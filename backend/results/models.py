from django.db import models
from students.models import Student, Subject
from faculty.models import Faculty

class Result(models.Model):
    result_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    grade = models.CharField(max_length=5, blank=True, null=True)
    semester = models.IntegerField()
    academic_year = models.CharField(max_length=10)
    is_published = models.BooleanField(default=False)
    entered_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'subject', 'semester')
        
    def __str__(self):
        return f"{self.student.roll_number} - {self.subject.subject_code} - {self.marks_obtained}/{self.max_marks}"
