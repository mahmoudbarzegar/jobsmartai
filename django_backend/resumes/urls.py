from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter(trailing_slash=False)
router.register('', ResumeViewSet, basename='resumes')

urlpatterns = router.urls
