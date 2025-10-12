from django.db import models
from django.conf import settings


class RankingResult(models.Model):
    """Ranking result model to store CV ranking results against JDs."""
    
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ranking_results')
    job_description = models.ForeignKey('job_descriptions.JobDescription', on_delete=models.CASCADE, related_name='ranking_results')
    
    # Store results as JSON
    results = models.JSONField(default=list, help_text="Array of ranking results")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    error = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ranking_results'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['job_description']),
        ]
    
    def __str__(self):
        return f"Ranking for {self.job_description.title} - {self.status}"


class UpgradeRequest(models.Model):
    """Model to track plan upgrade requests."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='upgrade_requests')
    current_plan = models.ForeignKey('plans.Plan', on_delete=models.SET_NULL, null=True, blank=True, related_name='upgrade_requests_from')
    requested_plan = models.ForeignKey('plans.Plan', on_delete=models.CASCADE, related_name='upgrade_requests_to')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, default='')
    admin_notes = models.TextField(blank=True, default='')
    
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_upgrade_requests')
    processed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'upgrade_requests'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.requested_plan.name} - {self.status}"
