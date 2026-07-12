from django.db import models
from authentication.models import User

class Notification(models.Model):
    TARGET_CHOICES = (
        ('all', 'All'),
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    )
    
    TYPE_CHOICES = (
        ('info', 'Info'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    )

    notification_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
    related_module = models.CharField(max_length=100, blank=True, null=True)
    target_role = models.CharField(max_length=20, choices=TARGET_CHOICES, default='all')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='targeted_notifications')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_notifications')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.target_role})"

class NotificationRead(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('notification', 'user')

    def __str__(self):
        return f"{self.user.email} read {self.notification.title}"

class NotificationDeleted(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deleted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('notification', 'user')

    def __str__(self):
        return f"{self.user.email} deleted {self.notification.title}"
