from django.db import models

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    homepage_url = models.URLField(max_length=500, blank=True, null=True)
    has_homepage = models.CharField(max_length=1, choices=[('O', 'Yes'), ('X', 'No')], default='X')
    has_policy = models.CharField(max_length=1, choices=[('O', 'Yes'), ('X', 'No')], default='X')
    policy_name_use = models.CharField(max_length=1, choices=[('O', 'Yes'), ('X', 'No')], default='X')
    processing_purpose = models.CharField(max_length=1, choices=[('O', 'Yes'), ('F', 'Partially'), ('X', 'No')], default='X')
    processed_items = models.CharField(max_length=1, choices=[('O', 'Yes'), ('F', 'Partially'), ('X', 'No')], default='X')
    consent_and_legal_basis = models.CharField(max_length=1, choices=[('O', 'Yes'), ('X', 'No')], default='X')
    retention_period = models.CharField(max_length=1, choices=[('O', 'Yes'), ('F', 'Partially'), ('X', 'No')], default='X')
    destruction_procedure = models.CharField(max_length=1, choices=[('O', 'Yes'), ('X', 'No')], default='X')
    third_party_provision = models.CharField(max_length=1, choices=[('O', 'Yes'), ('X', 'No')], default='X')
    consignment = models.CharField(max_length=1, choices=[('O', 'Yes'), ('X', 'No')], default='X')
    safety_measures = models.CharField(max_length=1, choices=[('O', 'Yes'), ('X', 'No')], default='X')
    auto_collection_device = models.CharField(max_length=1, choices=[('O', 'Yes'), ('X', 'No')], default='X')
    subject_rights = models.CharField(max_length=1, choices=[('O', 'Yes'), ('X', 'No')], default='X')
    responsible_person = models.CharField(max_length=1, choices=[('O', 'Yes'), ('F', 'Partially'), ('X', 'No')], default='X')
    relief_methods = models.CharField(max_length=1, choices=[('O', 'Yes'), ('X', 'No')], default='X')
    video_processing = models.CharField(max_length=1, choices=[('O', 'Yes'), ('X', 'No')], default='X')
    policy_changes = models.CharField(max_length=1, choices=[('O', 'Yes'), ('X', 'No')], default='X')


    def __str__(self):
        return self.name
