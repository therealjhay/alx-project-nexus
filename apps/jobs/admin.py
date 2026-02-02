from django.contrib import admin
from .models import JobCategory, JobPosting, Application

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)} # Auto-fill slug from name

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['title', 'employer', 'category', 'location', 'is_active', 'created_at']
    list_filter = ['is_active', 'category', 'job_type']
    search_fields = ['title', 'description', 'location']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'applied_at']
    list_filter = ['status']