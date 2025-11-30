from django.db import models

import uuid
from django.db import models
from django.urls import reverse
from django.utils import timezone

class Staff(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('expired', 'Expired'),
    ]
    
    DEPARTMENT_CHOICES = [
        ('medical', 'Medical'),
        ('nursing', 'Nursing'),
        ('admin', 'Administration'),
        ('lab', 'Laboratory'),
        ('pharmacy', 'Pharmacy'),
        ('radiology', 'Radiology'),
        ('support', 'Support Services'),
    ]
    
    # Unique identifier
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # Personal Information
    staff_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='staff_photos/', blank=True, null=True)
    
    # QR Code
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    
    # Employment Details
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    position = models.CharField(max_length=100)
    date_joined = models.DateField()
    date_expiry = models.DateField(blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Staff"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.staff_id} - {self.get_full_name()}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_verification_url(self):
        return reverse('staff:verify', kwargs={'uuid': self.uuid})
    
    def is_expired(self):
        if self.date_expiry:
            return timezone.now().date() > self.date_expiry
        return False
    
    def get_status_display_class(self):
        if self.status == 'active' and not self.is_expired():
            return 'success'
        return 'danger'
    
    def save(self, *args, **kwargs):
        """Generate QR code on save"""
        super().save(*args, **kwargs)
        
        # Generate QR code if it doesn't exist
        if not self.qr_code:
            from .utils import generate_qr_code
            qr_path = generate_qr_code(self, save_to_file=True)
            self.qr_code = qr_path
            super().save(update_fields=['qr_code'])

from django.contrib.auth.models import User

class VerificationLog(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='verification_logs')
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    verified_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-verified_at']
    
    def __str__(self):
        return f"{self.staff.staff_id} verified at {self.verified_at}"