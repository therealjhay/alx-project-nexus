from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField

class JobCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, help_text="Unique URL identifier")

    class Meta:
        verbose_name_plural = "Job Categories"

    def __str__(self):
        return self.name

class JobPosting(models.Model):
    class JobType(models.TextChoices):
        FULL_TIME = 'FULL_TIME', _('Full Time')
        PART_TIME = 'PART_TIME', _('Part Time')
        CONTRACT = 'CONTRACT', _('Contract')
        INTERNSHIP = 'INTERNSHIP', _('Internship')

    title = models.CharField(max_length=200)
    description = models.TextField()
    # Relations
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, related_name='jobs')
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_jobs')
    
    # Details
    location = models.CharField(max_length=100)
    salary_range = models.CharField(max_length=100, blank=True)
    job_type = models.CharField(max_length=20, choices=JobType.choices, default=JobType.FULL_TIME)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 1. Indexes allow O(1) or O(log n) lookups instead of O(n) table scans
        indexes = [
            GinIndex(
                name='job_posting_search_idx', 
                fields=['title', 'description'], 
                opclasses=['gin_trgm_ops', 'gin_trgm_ops']
            ),
        ]
        # 2. Orders by newest first by default
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.location}"

class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        ACCEPTED = 'ACCEPTED', _('Accepted')
        REJECTED = 'REJECTED', _('Rejected')

    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent spam: One application per job per user
        unique_together = ('job', 'applicant')

    def __str__(self):
        return f"{self.applicant} -> {self.job}"