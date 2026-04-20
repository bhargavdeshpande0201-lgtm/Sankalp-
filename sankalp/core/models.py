from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import secrets


class Complaint(models.Model):
    CATEGORY_CHOICES = [
        ('Waste', 'Waste Management'),
        ('Parking', 'Parking Issues'),
        ('Infrastructure', 'Infrastructure Damage'),
        ('Security', 'Security Incident'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Rejected', 'Rejected'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_complaints')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    location = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='complaints/', null=True, blank=True)
    anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.user} on {self.complaint}"


class EmailVerificationToken(models.Model):
    """Email verification token for new user registration"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_verification')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_valid(self):
        """Token valid for 24 hours"""
        return timezone.now() < self.created_at + timedelta(hours=24)
    
    def __str__(self):
        return f"Email verification for {self.user.username}"
    
    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(32)


class PasswordResetToken(models.Model):
    """Password reset token for forgot password functionality"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    
    def is_valid(self):
        """Token valid for 1 hour and not used"""
        return not self.used and timezone.now() < self.created_at + timedelta(hours=1)
    
    def __str__(self):
        return f"Password reset for {self.user.username}"
    
    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(32)
