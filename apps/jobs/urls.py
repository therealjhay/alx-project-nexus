from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobCategoryViewSet, JobPostingViewSet, ApplicationViewSet

router = DefaultRouter()
router.register(r'categories', JobCategoryViewSet)

# FIX: We added basename='postings' here so the router knows how to name the URL
router.register(r'postings', JobPostingViewSet, basename='postings')

router.register(r'applications', ApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
]