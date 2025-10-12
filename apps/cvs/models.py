from django.db import models
from django.conf import settings


class CV(models.Model):
    """CV/Resume model."""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cvs')
    filename = models.CharField(max_length=255)
    content = models.TextField(help_text="Extracted text content from PDF")
    file_path = models.CharField(max_length=500, null=True, blank=True)
    file_size = models.IntegerField(null=True, blank=True, help_text="File size in bytes")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cvs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.filename} - {self.user.email}"
