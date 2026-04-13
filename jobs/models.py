from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PhoneOTP(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.phone_number} - {self.otp}"
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# 2. JOB MODEL
class Job(models.Model):
    # Gender Choices
    GENDER_CHOICES = [
        ('Any', 'Male / Female'),
        ('Male', 'Male Only'),
        ('Female', 'Female Only'),
    ]

    # Core Information
    title = models.CharField(max_length=200) # e.g., "SALES STAFF", "LIGHT PETROL MECHANIC"
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='jobs')
    company_name = models.CharField(max_length=200, blank=True, null=True) # E.g., "Gas Stove Agency"
    location = models.CharField(max_length=150) # e.g., "Kondotty", "Oman"
    
    # Details from your WhatsApp format
    description = models.TextField(help_text="Main Malayalam/English description")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Any')
    salary = models.CharField(max_length=100) # e.g., "13600 + incentive" or "38000 to 43000"
    experience = models.CharField(max_length=100, blank=True, null=True) # e.g., "Freshers & Experience" or "2 year or 3 year"
    timing = models.CharField(max_length=100, blank=True, null=True) # e.g., "09.30 am to 05.00 pm"
    
    # Extra Perks & Requirements
    benefits = models.TextField(blank=True, null=True, help_text="e.g., ESI & PF, Food & Accommodation")
    requirements = models.TextField(blank=True, null=True, help_text="e.g., Two wheeler must, Arabic knowledge must")
    
    # Status & Contact
    is_urgent = models.BooleanField(default=False, help_text="Check this to show 📢 URGENT VACANCY tag")
    contact_info = models.CharField(max_length=100) # e.g., "8590667410"
    
    # System fields
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.location}"
    
class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending Review'),
        ('Reviewed', 'Reviewed'),
        ('Interview', 'Interviewing'),
        ('Onboarding', 'Hired / Onboarding'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    # --- NEW: PRIVATE ADMIN NOTES ---
    admin_notes = models.TextField(blank=True, help_text="Private notes hidden from the candidate.")
    rating = models.IntegerField(default=0, help_text="1 to 5 star rating.")
    # -------------------------------

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    resume_link = models.URLField(blank=True)
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant_name} applied for {self.job.title}"