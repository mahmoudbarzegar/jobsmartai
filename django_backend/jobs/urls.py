from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ApplicationViewSet, FindBestResumes, JobViewSet, ResumeViewSet

router = DefaultRouter(trailing_slash=False)
router.register("resumes", ResumeViewSet, basename="resumes")
router.register("jobs", JobViewSet, basename="job")
router.register("applications", ApplicationViewSet, basename="application")


urlpatterns = router.urls + [
    path("find-best-resumes/<int:job_id>", FindBestResumes.as_view()),
]
