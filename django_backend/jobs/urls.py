from rest_framework.routers import DefaultRouter

from .views import ApplicationViewSet, JobViewSet, ResumeViewSet

router = DefaultRouter(trailing_slash=False)
router.register("resumes", ResumeViewSet, basename="resumes")
router.register("jobs", JobViewSet, basename="job")
router.register("applications", ApplicationViewSet, basename="application")

urlpatterns = router.urls
