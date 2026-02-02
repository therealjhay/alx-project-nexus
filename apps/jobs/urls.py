from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobCategoryViewSet, JobPostingViewSet, ApplicationViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'categories', JobCategoryViewSet)
router.register(r'postings', JobPostingViewSet)
router.register(r'applications', ApplicationViewSet, basename='application')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]