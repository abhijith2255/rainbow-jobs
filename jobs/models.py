from django.db import models
from django.contrib.auth.models import User

# Details for the hiring companies
class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name

# Profiles for the candidates
class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

# The actual job listings
class JobPosting(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    salary = models.CharField(max_length=100, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# The bridge linking a candidate to a job
class Application(models.Model):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    applicant = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.user.username} applied for {self.job.title}"