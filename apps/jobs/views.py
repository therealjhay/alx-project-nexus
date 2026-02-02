from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import PermissionDenied
from .models import JobCategory, JobPosting, Application
from .serializers import JobCategorySerializer, JobPostingSerializer, ApplicationSerializer

class JobCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only for everyone. Only Admins should create categories (via Django Admin).
    """
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    permission_classes = [permissions.AllowAny]

class JobPostingViewSet(viewsets.ModelViewSet):
    """
    - Read: AllowAny
    - Write: Authenticated Users only (Ideally Employers)
    """
    queryset = JobPosting.objects.filter(is_active=True)
    serializer_class = JobPostingSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['created_at', 'salary_range']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        # Security: Auto-assign the current user as the employer
        serializer.save(employer=self.request.user)

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Security: 
        1. Applicants see ONLY their own applications.
        2. Employers see applications ONLY for their jobs.
        """
        user = self.request.user
        if user.role == 'EMPLOYER':
            return Application.objects.filter(job__employer=user)
        return Application.objects.filter(applicant=user)

    def perform_create(self, serializer):
        # Security: Auto-assign the applicant
        # Check if already applied
        job = serializer.validated_data['job']
        if Application.objects.filter(job=job, applicant=self.request.user).exists():
             raise PermissionDenied("You have already applied for this job.")
        
        serializer.save(applicant=self.request.user)