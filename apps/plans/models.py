from django.db import models


class Plan(models.Model):
    """Subscription plan model."""
    
    PLAN_NAMES = [
        ('Freemium', 'Freemium'),
        ('Starter', 'Starter'),
        ('Growth', 'Growth'),
        ('Pro', 'Pro'),
        ('Enterprise', 'Enterprise'),
    ]
    
    REGIONS = [
        ('Pakistan', 'Pakistan'),
        ('International', 'International'),
        ('Global', 'Global'),
    ]
    
    BILLING_CYCLES = [
        ('Monthly', 'Monthly'),
        ('SixMonth', 'Six Month'),
        ('Annual', 'Annual'),
    ]
    
    name = models.CharField(max_length=50, choices=PLAN_NAMES)
    region = models.CharField(max_length=50, choices=REGIONS)
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CYCLES, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default='USD')
    
    # Limits (-1 or NULL means unlimited)
    jd_limit = models.IntegerField(null=True, blank=True, help_text="Job Description limit (-1 or null for unlimited)")
    cv_limit = models.IntegerField(null=True, blank=True, help_text="CV limit (-1 or null for unlimited)")
    
    description = models.TextField(blank=True, default='')
    features = models.JSONField(default=list, blank=True)
    
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'plans'
        unique_together = ['name', 'region', 'billing_cycle']
        ordering = ['region', 'sort_order', 'name']
        indexes = [
            models.Index(fields=['name', 'region']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        if self.billing_cycle:
            return f"{self.name} ({self.billing_cycle}) - {self.region}"
        return f"{self.name} - {self.region}"
    
    @property
    def display_name(self):
        """Get display name for the plan."""
        if self.name == 'Freemium':
            return 'Freemium'
        if self.billing_cycle:
            return f"{self.name} ({self.billing_cycle})"
        return self.name
    
    def is_unlimited(self, limit_type):
        """Check if plan has unlimited usage."""
        if self.name == 'Enterprise':
            return True
        if limit_type == 'jd':
            return self.jd_limit is None or self.jd_limit == -1
        if limit_type == 'cv':
            return self.cv_limit is None or self.cv_limit == -1
        return False
    
    def save(self, *args, **kwargs):
        """Set currency based on region if not provided."""
        if not self.currency:
            self.currency = 'PKR' if self.region == 'Pakistan' else 'USD'
        super().save(*args, **kwargs)
