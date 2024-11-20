from django.db import models

class Policy(models.Model):
    hospital_name = models.CharField(max_length=255)
    effective_date = models.DateField()
    privacy_manager = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=255)
    
    has_privacy_department = models.BooleanField(default=False)
    privacy_department = models.CharField(max_length=255, blank=True, null=True)
    department_phone = models.CharField(max_length=20, blank=True, null=True)
    department_email = models.EmailField(blank=True, null=True)
    department_fax = models.CharField(max_length=20, blank=True, null=True)
    
    cctv = models.BooleanField(default=False)
    delegate = models.CharField(max_length=50, choices=[('no_delegate', 'No Delegate'), ('delegate', 'Delegate')], default='no_delegate')
    no_delegate_details = models.CharField(max_length=255, blank=True, null=True)
    
    # Add fields for storing sections and features as JSON or relational models
    sections = models.JSONField(blank=True, null=True)
    feature_data = models.JSONField(blank=True, null=True)
    consent_info = models.JSONField(blank=True, null=True)
    extra_rows = models.JSONField(blank=True, null=True)
    previous_policy_links = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return self.hospital_name
