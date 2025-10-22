from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter(trailing_slash=False)
router.register('resumes', ResumeViewSet, basename='resumes')
router.register('jobs', JobViewSet, basename='job')

urlpatterns = router.urls
