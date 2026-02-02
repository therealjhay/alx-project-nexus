from rest_framework import serializers
from .models import JobCategory, JobPosting, Application

class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ['id', 'name', 'slug']

class JobPostingSerializer(serializers.ModelSerializer):
    # We use StringRelatedField to show the category name instead of just ID in reads
    # But for writing, we'll need the ID. This is a common pattern.
    category_name = serializers.CharField(source='category.name', read_only=True)
    employer_email = serializers.CharField(source='employer.email', read_only=True)

    class Meta:
        model = JobPosting
        fields = [
            'id', 'title', 'description', 'category', 'category_name', 
            'employer_email', 'location', 'salary_range', 
            'job_type', 'created_at'
        ]
        # Security: Employer cannot be spoofed; it's set by the view automatically
        read_only_fields = ['employer', 'created_at']

class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    applicant_email = serializers.CharField(source='applicant.email', read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'job', 'job_title', 'applicant_email', 'cover_letter', 'status', 'applied_at']
        read_only_fields = ['applicant', 'status', 'applied_at']
    
    def validate_job(self, value):
        """Security Check: Ensure the job is actually active."""
        if not value.is_active:
            raise serializers.ValidationError("This job posting is closed.")
        return value