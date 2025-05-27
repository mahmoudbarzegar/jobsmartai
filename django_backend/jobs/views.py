from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .utils import search_jobs_from_remoteok
from resumes.models import ResumeModel


@extend_schema(
    tags=["Jobs"]
)
class JobViewSet(viewsets.ModelViewSet):
    http_method_names = ['post']

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "resume_id": {
                        "type": "integer"
                    }
                },
                "required": ["resume_id"]
            }
        },
    )
    @action(detail=False, methods=['post'], url_path='search')
    def search(self, request, *args, **kwargs):
        resume = ResumeModel.objects.get(id=request.data['resume_id'])
        jobs = search_jobs_from_remoteok(resume.resume_info['latest_job_title'], resume.resume_info['skills'])
        return Response({'status': 'success', 'result': {"jobs": jobs}}, status=status.HTTP_200_OK)
