from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q  # <--- CHANGED: Use standard Q objects instead of SearchVector
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import JobCategory, JobPosting, Application
from .serializers import JobCategorySerializer, JobPostingSerializer, ApplicationSerializer

class JobCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    permission_classes = [permissions.AllowAny]

class JobPostingViewSet(viewsets.ModelViewSet):
    """
    - Read: AllowAny
    - Write: Authenticated Users only (Employers)
    """
    serializer_class = JobPostingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='search',
                description='Search jobs by title or description',
                required=False,
                type=OpenApiTypes.STR
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        """
        Standard Search (Works on SQLite & Postgres)
        """
        queryset = JobPosting.objects.filter(is_active=True)
        search_query = self.request.query_params.get('search', None)

        if search_query:
            # CHANGED: Use Q objects for standard "contains" search
            return queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        return queryset

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'EMPLOYER':
            return Application.objects.filter(job__employer=user)
        return Application.objects.filter(applicant=user)

    def perform_create(self, serializer):
        job = serializer.validated_data['job']
        if Application.objects.filter(job=job, applicant=self.request.user).exists():
             raise PermissionDenied("You have already applied for this job.")
        serializer.save(applicant=self.request.user)